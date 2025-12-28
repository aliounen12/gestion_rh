#!/usr/bin/env python3
"""
Fonctions de base de données PostgreSQL pour ChatRH
"""

from typing import Dict, List, Optional
import sys

# Import optionnel de psycopg2 - gère l'absence gracieusement
try:
import psycopg2
import psycopg2.extras
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith('utf'):
        print("⚠️ psycopg2-binary non disponible - PostgreSQL désactivé")
    else:
        print("Warning: psycopg2-binary not available - PostgreSQL disabled")

from app.config import settings

def get_db_connection():
    """
    Obtient une connexion à la base de données PostgreSQL
    
    Returns:
        Connection object ou None si la connexion échoue
    """
    if not PSYCOPG2_AVAILABLE:
        return None
    
    try:
        connection = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            client_encoding='UTF8'
        )
        return connection
    except Exception as e:
        print(f"Erreur de connexion à PostgreSQL: {e}")
        return None

def get_articles_by_sujet(id_sujet: int) -> List[Dict]:
    """
    Récupère tous les articles d'un sujet donné
    
    Args:
        id_sujet: L'ID du sujet
    
    Returns:
        Liste de dictionnaires contenant les articles
    """
    if not PSYCOPG2_AVAILABLE:
        return []
    
    connection = get_db_connection()
    if not connection:
        return []
    
    articles = []
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT article_id, id_sujet, num_article, source, contenu "
            "FROM public.article "
            "WHERE id_sujet = %s "
            "ORDER BY article_id ASC",
            (id_sujet,)
        )
        
        for row in cursor.fetchall():
            articles.append({
                "article_id": row['article_id'],
                "id_sujet": row['id_sujet'],
                "num_article": row['num_article'],
                "source": row['source'],
                "contenu": row['contenu']
            })
    except Exception as e:
        print(f"Erreur lors de la récupération des articles: {e}")
    finally:
        if connection:
        cursor.close()
        connection.close()
    
    return articles

def get_article_by_id(article_id: int) -> Optional[Dict]:
    """
    Récupère un article par son ID
    
    Args:
        article_id: L'ID de l'article
    
    Returns:
        Dictionnaire contenant l'article ou None
    """
    if not PSYCOPG2_AVAILABLE:
        return None
    
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT article_id, id_sujet, num_article, source, contenu "
            "FROM public.article "
            "WHERE article_id = %s",
            (article_id,)
        )
        
        row = cursor.fetchone()
        if row:
            return {
                "article_id": row['article_id'],
                "id_sujet": row['id_sujet'],
                "num_article": row['num_article'],
                "source": row['source'],
                "contenu": row['contenu']
            }
    except Exception as e:
        print(f"Erreur lors de la récupération de l'article: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    
    return None

def search_articles(keyword: str, limit: int = 10) -> List[Dict]:
    """
    Recherche des articles par mot-clé dans le contenu
    
    Args:
        keyword: Mot-clé à rechercher
        limit: Nombre maximum de résultats
    
    Returns:
        Liste de dictionnaires contenant les articles correspondants
    """
    if not PSYCOPG2_AVAILABLE:
        return []
    
    connection = get_db_connection()
    if not connection:
        return []
    
    articles = []
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT article_id, id_sujet, num_article, source, contenu "
            "FROM public.article "
            "WHERE LOWER(contenu) LIKE %s OR LOWER(num_article) LIKE %s "
            "ORDER BY article_id ASC "
            "LIMIT %s",
            (f"%{keyword.lower()}%", f"%{keyword.lower()}%", limit)
        )
        
        for row in cursor.fetchall():
            articles.append({
                "article_id": row['article_id'],
                "id_sujet": row['id_sujet'],
                "num_article": row['num_article'],
                "source": row['source'],
                "contenu": row['contenu']
            })
    except Exception as e:
        print(f"Erreur lors de la recherche d'articles: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    
    return articles

def get_all_sujets() -> List[Dict]:
    """
    Récupère tous les sujets
    
    Returns:
        Liste de dictionnaires contenant les sujets
    """
    if not PSYCOPG2_AVAILABLE:
        return []
    
    connection = get_db_connection()
    if not connection:
        return []
    
    sujets = []
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT id, titre_sujet, description "
            "FROM public.sujet "
            "ORDER BY id ASC"
        )
        
        for row in cursor.fetchall():
            sujets.append({
                "id": row['id'],
                "titre_sujet": row['titre_sujet'],
                "description": row['description']
            })
    except Exception as e:
        print(f"Erreur lors de la récupération des sujets: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    
    return sujets

def get_sujet_by_id(sujet_id: int) -> Optional[Dict]:
    """
    Récupère un sujet par son ID
    
    Args:
        sujet_id: L'ID du sujet
    
    Returns:
        Dictionnaire contenant le sujet ou None
    """
    if not PSYCOPG2_AVAILABLE:
        return None
    
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT id, titre_sujet, description "
            "FROM public.sujet "
            "WHERE id = %s",
            (sujet_id,)
        )
        
        row = cursor.fetchone()
        if row:
            return {
                "id": row['id'],
                "titre_sujet": row['titre_sujet'],
                "description": row['description']
            }
    except Exception as e:
        print(f"Erreur lors de la récupération du sujet: {e}")
    finally:
        if connection:
        cursor.close()
        connection.close()
    
    return None

def get_articles_count() -> int:
    """
    Retourne le nombre total d'articles dans la base de données
    
    Returns:
        Nombre d'articles
    """
    if not PSYCOPG2_AVAILABLE:
        return 0
    
    connection = get_db_connection()
    if not connection:
        return 0
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM public.article")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print(f"Erreur lors du comptage des articles: {e}")
        return 0
    finally:
        if connection:
        cursor.close()
        connection.close()
