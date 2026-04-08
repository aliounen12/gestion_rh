"""
Module LLM - Client pour les services d'IA
"""

from .openrouter_client import OpenRouterClient, resolve_openrouter_model

# Instance globale du client
openrouter_client = OpenRouterClient()

__all__ = ["openrouter_client", "OpenRouterClient", "resolve_openrouter_model"]
