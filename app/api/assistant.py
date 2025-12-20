#!/usr/bin/env python3
"""
Router simplifié pour l'assistant - 3 endpoints seulement
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from app.llm import openrouter_client
from app.config import settings

# Router pour l'assistant
assistant_router = APIRouter(prefix="/assistant", tags=["assistant"])

# Schémas pour les requêtes/réponses
class ChatRequest(BaseModel):
    """Requête pour le chat avec l'assistant"""
    message: str
    model: Optional[str] = None
    temperature: Optional[float] = None

class ChatResponse(BaseModel):
    """Réponse du chat"""
    response: str
    model: str

class Tool(BaseModel):
    """Outil disponible"""
    name: str
    description: str
    type: str

class ToolsResponse(BaseModel):
    """Liste des outils disponibles"""
    tools: List[Tool]

class HealthResponse(BaseModel):
    """Réponse du health check"""
    status: str
    message: str

@assistant_router.post("/chat", response_model=ChatResponse)
def chat_with_assistant(request: ChatRequest):
    """
    Chat With Assistant
    
    Permet de discuter avec l'assistant IA pour obtenir des informations sur la gestion des primes
    et le Code du travail sénégalais.
    """
    try:
        system_prompt = """Tu es un assistant expert en gestion des ressources humaines et en droit du travail sénégalais.
Tu aides les utilisateurs à comprendre les primes, le Code du travail et la conformité légale.
Réponds toujours en français de manière claire et professionnelle."""
        
        response = openrouter_client.chat_completion(
            prompt=request.message,
            system_prompt=system_prompt,
            model=request.model,
            temperature=request.temperature
        )
        
        return ChatResponse(
            response=response,
            model=request.model or settings.OPENROUTER_MODEL
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du chat: {str(e)}")

@assistant_router.get("/tools", response_model=ToolsResponse)
def get_available_tools():
    """
    Get Available Tools
    
    Retourne la liste des outils disponibles pour l'assistant.
    """
    tools = [
        Tool(
            name="chat",
            description="Chat avec l'assistant IA pour obtenir des informations sur la gestion des primes et le Code du travail",
            type="chat"
        ),
        Tool(
            name="analyze_prime",
            description="Analyser une prime pour vérifier sa conformité légale",
            type="analysis"
        ),
        Tool(
            name="explain_article",
            description="Expliquer un article du Code du travail sénégalais",
            type="explanation"
        ),
        Tool(
            name="search_articles",
            description="Rechercher des articles du Code du travail par mot-clé",
            type="search"
        )
    ]
    
    return ToolsResponse(tools=tools)

# Router pour le health check
health_router = APIRouter(tags=["health"])

@health_router.get("/gestionrh", response_model=HealthResponse)
def health_check():
    """
    Health Check
    
    Vérifie l'état de l'API de gestion RH.
    """
    try:
        from app.db import code_articles
        
        return HealthResponse(
            status="ok",
            message=f"API Gestion RH opérationnelle - {len(code_articles)} articles chargés"
        )
    except Exception as e:
        return HealthResponse(
            status="error",
            message=f"Erreur: {str(e)}"
        )

