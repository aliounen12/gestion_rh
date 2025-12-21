"""
Module LLM - Client pour les services d'IA
"""

from .openrouter_client import OpenRouterClient

# Instance globale du client
openrouter_client = OpenRouterClient()

__all__ = ["openrouter_client", "OpenRouterClient"]
