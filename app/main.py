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
        
        # Créer le prompt système avec contexte
        context = get_rh_context(topic)
        system_prompt = create_system_prompt(context)
        
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
    
    Vérifie l'état de l'API ChatRH.
    """
    return HealthResponse(
        status="ok",
        message="API ChatRH opérationnelle"
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
