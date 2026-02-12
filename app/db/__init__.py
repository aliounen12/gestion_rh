"""
Module DB - Accès aux données du Code du travail

Par défaut, l'application utilise le fichier DOCX `Code_du_travail_SN` comme source.
"""

from .db_code_travail_docx import (
    get_db_connection,
    get_articles_by_sujet,
    get_article_by_id,
    get_article_by_num_article,
    search_articles,
    get_all_sujets,
    get_sujet_by_id,
    get_articles_count
)

__all__ = [
    "get_db_connection",
    "get_articles_by_sujet",
    "get_article_by_id",
    "get_article_by_num_article",
    "search_articles",
    "get_all_sujets",
    "get_sujet_by_id",
    "get_articles_count"
]
