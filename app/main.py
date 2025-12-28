#!/usr/bin/env python3
"""
Application FastAPI principale pour ChatRH
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.config import settings
from app.llm import openrouter_client
from app.tools import (
    create_system_prompt,
    format_chat_response,
    validate_message,
    get_rh_context,
    extract_keywords
)
from app.db import get_articles_count

# Création de l'application FastAPI
app = FastAPI(
    title="ChatRH API",
    description="API de chat pour la gestion des ressources humaines",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schémas pour les requêtes/réponses
class ChatRequest(BaseModel):
    """Requête pour le chat"""
    message: str
    model: Optional[str] = None
    temperature: Optional[float] = None

class ChatResponse(BaseModel):
    """Réponse du chat"""
    response: str
    model: str

class HealthResponse(BaseModel):
    """Réponse du health check"""
    status: str
    message: str

# Endpoint racine
@app.get("/")
def root():
    """Endpoint racine avec informations sur l'API"""
    return {
        "name": "ChatRH API",
        "version": "1.0.0",
        "description": "API de chat pour la gestion des ressources humaines",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs"
        }
    }

# Endpoint chat
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Chat avec l'assistant IA
    
    Permet de discuter avec l'assistant pour obtenir des informations
    sur la gestion des ressources humaines.
    """
    try:
        # Valider le message
        is_valid, error_message = validate_message(request.message)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)
        
        # Extraire les mots-clés pour le contexte
        keywords = extract_keywords(request.message)
        topic = keywords[0] if keywords else None
        
        # Rechercher des articles pertinents dans la base de données
        relevant_articles = []
        try:
            from app.db import search_articles, get_articles_by_sujet, get_all_sujets
            
            # Étape 1 : Chercher par sujet si identifié
            sujets = get_all_sujets()
            sujet_trouve = None
            
            # Chercher dans les keywords
            for keyword in keywords:
                for sujet in sujets:
                    if keyword.lower() in sujet['titre_sujet'].lower() or str(sujet['id']) == keyword:
                        sujet_trouve = sujet
                        articles = get_articles_by_sujet(sujet['id'])
                        relevant_articles.extend(articles)
                        break
                if sujet_trouve:
                    break
            
            # Étape 2 : Si pas de sujet trouvé, chercher dans le message directement
            if not sujet_trouve:
                message_lower = request.message.lower()
                # Mapping direct des mots-clés vers les sujets
                keyword_mapping = {
                    "congé": "Congés",
                    "congés": "Congés",
                    "conges": "Congés",  # Sans accent
                    "transport": "Transport",
                    "tansport": "Transport"  # Typo
                }
                
                # Chercher les mots-clés dans le message
                for keyword, sujet_nom in keyword_mapping.items():
                    if keyword in message_lower:
                        for sujet in sujets:
                            if sujet['titre_sujet'] == sujet_nom:
                                sujet_trouve = sujet
                                articles = get_articles_by_sujet(sujet['id'])
                                relevant_articles.extend(articles)
                                break
                        if sujet_trouve:
                            break
                
                # Si toujours pas trouvé, chercher par titre de sujet
                if not sujet_trouve:
                    for sujet in sujets:
                        titre_lower = sujet['titre_sujet'].lower()
                        # Vérifier si le titre complet est dans le message
                        if titre_lower in message_lower:
                            sujet_trouve = sujet
                            articles = get_articles_by_sujet(sujet['id'])
                            relevant_articles.extend(articles)
                            break
                        # Vérifier si des mots du titre sont dans le message
                        elif any(word in message_lower for word in titre_lower.split() if len(word) > 3):
                            sujet_trouve = sujet
                            articles = get_articles_by_sujet(sujet['id'])
                            relevant_articles.extend(articles)
                            break
            
            # Étape 3 : Recherche par mot-clé dans le contenu des articles
            if not relevant_articles:
                # Extraire les mots importants du message (mots de 4+ caractères)
                words = [w for w in request.message.lower().split() if len(w) > 4]
                for word in words[:5]:  # Limiter à 5 mots
                    articles = search_articles(word, limit=5)
                    # Éviter les doublons
                    existing_ids = {a['article_id'] for a in relevant_articles}
                    for article in articles:
                        if article['article_id'] not in existing_ids:
                            relevant_articles.append(article)
                    if len(relevant_articles) >= 10:
                        break
            
            # Limiter à 10 articles maximum pour éviter un contexte trop long
            relevant_articles = relevant_articles[:10]
            
        except Exception as e:
            # Si erreur, continuer sans les articles
            print(f"Erreur lors de la recherche d'articles: {e}")
            relevant_articles = []
        
        # Construire le contexte avec les données PostgreSQL
        context = get_rh_context(topic)
        
        # Créer le prompt système avec les articles (CONTENU COMPLET)
        system_prompt = create_system_prompt(context, relevant_articles)
        
        # Appeler l'API OpenRouter
        response = openrouter_client.chat_completion(
            prompt=request.message,
            system_prompt=system_prompt,
            model=request.model,
            temperature=request.temperature
        )
        
        # Formater la réponse
        model_used = request.model or settings.OPENROUTER_MODEL
        formatted = format_chat_response(response, model_used)
        
        return ChatResponse(**formatted)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du chat: {str(e)}")

# Endpoint health check
@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health Check
    
    Vérifie l'état de l'API ChatRH et de la connexion PostgreSQL.
    """
    try:
        articles_count = get_articles_count()
        message = f"API ChatRH opérationnelle"
        if articles_count > 0:
            message += f" - {articles_count} articles disponibles dans la base de données"
        else:
            message += " - PostgreSQL non configuré ou base vide"
        
        return HealthResponse(
            status="ok",
            message=message
        )
    except Exception as e:
        return HealthResponse(
            status="ok",
            message=f"API ChatRH opérationnelle - Erreur base de données: {str(e)}"
        )

# Démarrage automatique du serveur (uniquement en local)
if __name__ == "__main__":
    import uvicorn
    print("🚀 Démarrage de l'API ChatRH")
    print(f"🌐 Serveur disponible sur: http://localhost:{settings.API_PORT}")
    print("📖 Documentation: http://localhost:8000/docs")
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
