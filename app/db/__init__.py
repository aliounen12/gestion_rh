"""
Module DB - Gestion de la base de données PostgreSQL
"""

from .db_postgres import (
    get_db_connection,
    get_articles_by_sujet,
    get_article_by_id,
    search_articles,
    get_all_sujets,
    get_sujet_by_id,
    get_articles_count
)

__all__ = [
    "get_db_connection",
    "get_articles_by_sujet",
    "get_article_by_id",
    "search_articles",
    "get_all_sujets",
    "get_sujet_by_id",
    "get_articles_count"
]
