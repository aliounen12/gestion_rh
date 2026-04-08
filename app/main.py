#!/usr/bin/env python3
"""
Application FastAPI principale pour ChatRH
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.config import settings
from app.llm import openrouter_client
from app.tools import (
    create_system_prompt,
    format_chat_response,
    validate_message,
    get_rh_context,
    extract_keywords,
    prepare_articles_for_chat,
    article_refs_for_chat_response,
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
    sources: Optional[List[Dict[str, Any]]] = None

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


@app.get("/articles/search")
def search_articles_endpoint(q: str = Query(..., min_length=1), limit: int = Query(5, ge=1, le=50)):
    """
    Recherche d'articles dans le Code du travail (contenu, libellé de chapitre, numéro).
    Exemples de requêtes: "congé", "L.148", "syndicat", "marques syndicales".
    """
    from app.db import search_articles
    results = search_articles(q, limit=limit)
    # Ne pas renvoyer le champ interne `contenu_norm`
    return [{k: v for k, v in a.items() if k != "contenu_norm"} for a in results]


@app.get("/articles/{num_article}")
def get_article_endpoint(num_article: str):
    """
    Récupère un article par numéro.
    Exemples: /articles/L.148 , /articles/148 , /articles/L148
    """
    from app.db import get_article_by_num_article

    article = get_article_by_num_article(num_article)
    if not article:
        raise HTTPException(status_code=404, detail="Article introuvable")
    return {k: v for k, v in article.items() if k != "contenu_norm"}


def _article_public(article: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in article.items() if k != "contenu_norm"}


@app.get("/sujets")
def list_sujets_endpoint():
    """Liste des titres (sujets) du Code du travail issus du DOCX."""
    from app.db import get_all_sujets
    return get_all_sujets()


@app.get("/sujets/{sujet_id}/chapitres")
def sujet_chapitres_endpoint(sujet_id: int):
    """
    Articles d'un titre regroupés par chapitre (sous-sections), pour navigation ou affichage structuré.
    Les articles placés avant le premier chapitre du titre sont dans `articles_sans_chapitre`.
    """
    from app.db import get_sujet_grouped_by_chapitre

    data = get_sujet_grouped_by_chapitre(sujet_id)
    if not data:
        raise HTTPException(status_code=404, detail="Sujet introuvable")
    return {
        "sujet": data["sujet"],
        "chapitres": [
            {
                **{k: v for k, v in bloc.items() if k != "articles"},
                "articles": [_article_public(a) for a in bloc["articles"]],
            }
            for bloc in data["chapitres"]
        ],
        "articles_sans_chapitre": [_article_public(a) for a in data["articles_sans_chapitre"]],
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
        
        # Rechercher des articles pertinents dans la source de données (fichier Code_du_travail_SN)
        relevant_articles: List[Dict[str, Any]] = []
        seen_article_ids: set = set()
        sujet_focus_id: Optional[int] = None

        def _add_articles(articles: List[Dict[str, Any]]) -> None:
            for article in articles:
                aid = article.get("article_id")
                if aid is None or aid in seen_article_ids:
                    continue
                seen_article_ids.add(aid)
                relevant_articles.append(article)

        try:
            from app.db import search_articles, get_articles_by_sujet, get_all_sujets

            msg_stripped = request.message.strip()
            # Pass 0 : recherche sur la phrase (contenu + chapitre) pour les questions courtes
            if msg_stripped and len(msg_stripped) <= 200:
                _add_articles(search_articles(msg_stripped, limit=8))

            sujets = get_all_sujets()
            sujet_trouve = None

            # Étape 1 : Chercher par sujet si identifié
            for keyword in keywords:
                for sujet in sujets:
                    if keyword.lower() in sujet["titre_sujet"].lower() or str(sujet["id"]) == keyword:
                        sujet_trouve = sujet
                        sujet_focus_id = sujet["id"]
                        _add_articles(get_articles_by_sujet(sujet["id"]))
                        break
                if sujet_trouve:
                    break

            # Étape 2 : Si pas de sujet trouvé, chercher dans le message directement
            if not sujet_trouve:
                message_lower = request.message.lower()
                keyword_mapping = {
                    "congé": "Congés",
                    "congés": "Congés",
                    "conges": "Congés",
                    "transport": "Transport",
                    "tansport": "Transport",
                }

                for keyword, sujet_nom in keyword_mapping.items():
                    if keyword in message_lower:
                        for sujet in sujets:
                            if sujet["titre_sujet"] == sujet_nom:
                                sujet_trouve = sujet
                                sujet_focus_id = sujet["id"]
                                _add_articles(get_articles_by_sujet(sujet["id"]))
                                break
                        if sujet_trouve:
                            break

                if not sujet_trouve:
                    for sujet in sujets:
                        titre_lower = sujet["titre_sujet"].lower()
                        if titre_lower in message_lower:
                            sujet_trouve = sujet
                            sujet_focus_id = sujet["id"]
                            _add_articles(get_articles_by_sujet(sujet["id"]))
                            break
                        if any(word in message_lower for word in titre_lower.split() if len(word) > 3):
                            sujet_trouve = sujet
                            sujet_focus_id = sujet["id"]
                            _add_articles(get_articles_by_sujet(sujet["id"]))
                            break

            # Étape 3 : Recherche par mot-clé dans le contenu / chapitres
            if not relevant_articles:
                words = [w for w in request.message.lower().split() if len(w) > 4]
                for word in words[:5]:
                    _add_articles(search_articles(word, limit=5))
                    if len(relevant_articles) >= 10:
                        break

            chat_limit = getattr(settings, "CHAT_MAX_ARTICLES", 8)
            relevant_articles = prepare_articles_for_chat(relevant_articles[:chat_limit])
            
        except Exception as e:
            # Si erreur, continuer sans les articles
            print(f"Erreur lors de la recherche d'articles: {e}")
            relevant_articles = []
            sujet_focus_id = None
        
        # Construire le contexte avec les données de la source (titres + chapitres si sujet identifié)
        context = get_rh_context(str(sujet_focus_id) if sujet_focus_id is not None else topic)
        
        # Créer le prompt système avec les articles (CONTENU COMPLET)
        system_prompt = create_system_prompt(context, relevant_articles)
        
        # Vérifier que la clé API est configurée
        if not settings.OPENROUTER_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="OPENROUTER_API_KEY n'est pas configurée. Veuillez configurer cette variable d'environnement dans Vercel Dashboard."
            )
        
        # Appeler l'API OpenRouter
        try:
            response = openrouter_client.chat_completion(
                prompt=request.message,
                system_prompt=system_prompt,
                model=request.model,
                temperature=request.temperature
            )
        except ValueError as e:
            # Erreur spécifique d'OpenRouter (401, 400 contexte / modèle, timeout, etc.)
            error_msg = str(e)
            if "401" in error_msg or "authentification" in error_msg.lower():
                raise HTTPException(
                    status_code=401,
                    detail="Erreur d'authentification OpenRouter. Vérifiez que votre clé API est valide dans Vercel Dashboard."
                )
            if "400" in error_msg or "requête refusée par openrouter (400)" in error_msg.lower():
                raise HTTPException(
                    status_code=400,
                    detail=error_msg,
                )
            elif "timeout" in error_msg.lower():
                raise HTTPException(
                    status_code=504,
                    detail="Timeout lors de l'appel à OpenRouter. Le service peut être surchargé, réessayez plus tard."
                )
            else:
                raise HTTPException(
                    status_code=502,
                    detail=f"Erreur lors de l'appel à OpenRouter: {error_msg}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"Erreur de connexion à OpenRouter: {str(e)}"
            )
        
        # Formater la réponse
        model_used = request.model or settings.OPENROUTER_MODEL
        formatted = format_chat_response(
            response,
            model_used,
            sources=article_refs_for_chat_response(relevant_articles) if relevant_articles else None,
        )

        return ChatResponse(**formatted)
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Erreur générale
        import traceback
        error_detail = str(e)
        print(f"Erreur inattendue: {error_detail}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement de la requête: {error_detail}"
        )

# Endpoint health check
@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health Check
    
    Vérifie l'état de l'API ChatRH et l'accès à la source de données (fichier).
    """
    try:
        articles_count = get_articles_count()
        message = f"API ChatRH opérationnelle"
        if articles_count > 0:
            message += f" - {articles_count} articles disponibles dans la source de données"
        else:
            message += " - Source de données indisponible ou vide"
        
        # Vérifier aussi la clé API OpenRouter
        if not settings.OPENROUTER_API_KEY:
            message += " - ⚠️ OPENROUTER_API_KEY non configurée"
        else:
            message += " - ✅ OpenRouter configuré"
        
        return HealthResponse(
            status="ok",
            message=message
        )
    except Exception as e:
        return HealthResponse(
            status="ok",
            message=f"API ChatRH opérationnelle - Erreur base de données: {str(e)}"
        )

# Endpoint de diagnostic
@app.get("/diagnostic")
def diagnostic():
    """
    Endpoint de diagnostic pour vérifier la configuration
    """
    diagnostic_info = {
        "api_status": "ok",
        "openrouter": {
            "api_key_configured": bool(settings.OPENROUTER_API_KEY),
            "api_key_length": len(settings.OPENROUTER_API_KEY) if settings.OPENROUTER_API_KEY else 0,
            "model": settings.OPENROUTER_MODEL,
            "api_url": settings.OPENROUTER_API_URL
        },
        "data_source": {
            "type": "docx_file",
            "code_travail_path": settings.CODE_TRAVAIL_PATH or "par défaut (Code_du_travail_SN à la racine du projet)"
        },
    }
    
    try:
        articles_count = get_articles_count()
        diagnostic_info["data_source"]["articles_count"] = articles_count
        diagnostic_info["data_source"]["loaded"] = True
    except Exception as e:
        diagnostic_info["data_source"]["loaded"] = False
        diagnostic_info["data_source"]["error"] = str(e)
    
    return diagnostic_info

# Démarrage automatique du serveur (uniquement en local)
if __name__ == "__main__":
    import uvicorn
    # Éviter les emojis: certaines consoles Windows (cp1252) lèvent UnicodeEncodeError
    print("Demarrage de l'API ChatRH")
    print(f"Serveur disponible sur: http://localhost:{settings.API_PORT}")
    print("Documentation: http://localhost:8000/docs")
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
