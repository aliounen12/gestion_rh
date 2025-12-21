#!/usr/bin/env python3
"""
Fonctions utilitaires pour le chat
"""

from typing import Optional

def create_system_prompt(context: Optional[str] = None) -> str:
    """
    Crée un prompt système pour l'assistant IA
    
    Args:
        context: Contexte additionnel à inclure dans le prompt
    
    Returns:
        Le prompt système formaté
    """
    base_prompt = """Tu es un assistant expert en gestion des ressources humaines.
Tu aides les utilisateurs à comprendre les pratiques RH, le droit du travail,
la gestion des primes, et la conformité légale.
Réponds toujours en français de manière claire et professionnelle."""
    
    if context:
        base_prompt += f"\n\nContexte additionnel: {context}"
    
    return base_prompt

def format_chat_response(response: str, model: str) -> dict:
    """
    Formate la réponse du chat
    
    Args:
        response: La réponse générée par le modèle
        model: Le modèle utilisé
    
    Returns:
        Un dictionnaire formaté avec la réponse
    """
    return {
        "response": response,
        "model": model
    }

def validate_message(message: str) -> tuple[bool, Optional[str]]:
    """
    Valide un message avant l'envoi
    
    Args:
        message: Le message à valider
    
    Returns:
        Un tuple (is_valid, error_message)
    """
    if not message or not message.strip():
        return False, "Le message ne peut pas être vide"
    
    if len(message) > 5000:
        return False, "Le message est trop long (maximum 5000 caractères)"
    
    return True, None
