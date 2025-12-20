"""
Module DB - Gestion de la base de données
"""

from .db_postgres import (
    code_articles,
    primes_db,
    find_relevant_articles,
    generate_explanations_from_articles,
    add_prime_to_db,
    get_prime_by_id,
    get_all_primes,
    get_primes_by_type,
    get_available_prime_types,
    get_article_by_code,
    search_articles_by_keyword,
    get_articles_count,
    get_db_connection,
    load_articles_from_postgres
)

__all__ = [
    "code_articles",
    "primes_db",
    "find_relevant_articles",
    "generate_explanations_from_articles",
    "add_prime_to_db",
    "get_prime_by_id",
    "get_all_primes",
    "get_primes_by_type",
    "get_available_prime_types",
    "get_article_by_code",
    "search_articles_by_keyword",
    "get_articles_count",
    "get_db_connection",
    "load_articles_from_postgres"
]

