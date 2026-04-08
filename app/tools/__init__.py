"""
Module Tools - Fonctions utilitaires pour ChatRH
"""

from .chat_functions import (
    create_system_prompt,
    format_chat_response,
    validate_message,
    prepare_articles_for_chat,
    article_refs_for_chat_response,
)
from .rh_helpers import (
    get_rh_context,
    format_rh_advice,
    extract_keywords
)

__all__ = [
    "create_system_prompt",
    "format_chat_response",
    "validate_message",
    "prepare_articles_for_chat",
    "article_refs_for_chat_response",
    "get_rh_context",
    "format_rh_advice",
    "extract_keywords"
]
