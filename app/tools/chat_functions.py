#!/usr/bin/env python3
"""
Fonctions utilitaires pour le chat
"""

from typing import Optional

def create_system_prompt(context: Optional[str] = None, articles: Optional[list] = None) -> str:
    """
    Crée un prompt système pour l'assistant IA
    
    Args:
        context: Contexte additionnel à inclure dans le prompt
        articles: Liste d'articles du Code du travail à utiliser
    
    Returns:
        Le prompt système formaté
    """
    base_prompt = """Tu es un assistant expert en gestion des ressources humaines et en droit du travail sénégalais.
Tu aides les utilisateurs à comprendre les pratiques RH, le droit du travail,
la gestion des primes, et la conformité légale.
Réponds TOUJOURS en français de manière claire et professionnelle.
    
IMPORTANT : Tu dois te baser UNIQUEMENT sur les articles du Code du travail fournis ci-dessous.
Si un article n'est pas fourni, indique que tu n'as pas cette information dans ta base de données.
Ne donne JAMAIS d'informations générales qui ne sont pas basées sur les articles fournis."""
    
    if articles and len(articles) > 0:
        base_prompt += "\n\n=== ARTICLES DU CODE DU TRAVAIL À UTILISER ===\n"
        for i, article in enumerate(articles, 1):
            base_prompt += f"\nArticle {i} - {article.get('num_article', 'N/A')} ({article.get('source', 'Code du travail')}):\n"
            base_prompt += f"{article.get('contenu', '')}\n"
        base_prompt += "\n=== FIN DES ARTICLES ===\n"
        base_prompt += "\nINSTRUCTION CRITIQUE : Réponds UNIQUEMENT en te basant sur les articles ci-dessus. "
        base_prompt += "Cite les numéros d'articles lorsque c'est pertinent. "
        base_prompt += "Si la question ne peut pas être répondue avec ces articles, dis-le clairement."
    
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
