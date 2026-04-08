"""
Accès aux données du Code du travail — source unique : fichier DOCX indexé en mémoire.
"""

from .db_code_travail_docx import (
    get_db_connection,
    get_articles_by_sujet,
    get_article_by_id,
    get_article_by_num_article,
    search_articles,
    get_all_sujets,
    get_sujet_by_id,
    get_sujet_grouped_by_chapitre,
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
    "get_sujet_grouped_by_chapitre",
    "get_articles_count"
]
