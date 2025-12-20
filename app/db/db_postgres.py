#!/usr/bin/env python3
"""
Fonctions de base de données PostgreSQL pour utiliser la table articles existante
"""

from typing import Dict, List, Optional

# Import optionnel de psycopg2 - gère l'absence gracieusement
try:
    import psycopg2
    import psycopg2.extras
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    print("⚠️ psycopg2-binary non disponible - PostgreSQL désactivé")

from app.config import settings

# Cache pour les articles (chargé une seule fois)
_articles_cache: Optional[Dict[str, str]] = None

def get_db_connection():
    """Obtient une connexion à la base de données PostgreSQL"""
    if not PSYCOPG2_AVAILABLE:
        print("⚠️ PostgreSQL non disponible - psycopg2-binary n'est pas installé")
        return None
    
    try:
        connection = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        return connection
    except Exception as e:
        print(f"Erreur de connexion à PostgreSQL: {e}")
        return None

def load_articles_from_postgres() -> Dict[str, str]:
    """Charge les articles depuis la table PostgreSQL public.articles"""
    global _articles_cache
    
    if _articles_cache is not None:
        return _articles_cache
    
    articles = {}
    connection = get_db_connection()
    
    if not connection:
        print("Impossible de se connecter à PostgreSQL")
        return articles
    
    try:
        if not PSYCOPG2_AVAILABLE:
            print("⚠️ PostgreSQL non disponible - articles non chargés")
            return articles
        
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT article_code, contenu FROM public.articles")
        
        for row in cursor.fetchall():
            article_code = row['article_code']
            content = row['contenu']
            # Nettoyer le contenu des caractères d'encodage problématiques
            content = content.replace('ï¿½', 'é').replace('Ã¯Â¿Â½', 'é')
            articles[article_code] = content
        
        print(f"✅ {len(articles)} articles chargés depuis PostgreSQL")
        
    except Exception as e:
        print(f"Erreur lors du chargement des articles: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    
    _articles_cache = articles
    return articles

def find_relevant_articles(prime_type: str) -> List[str]:
    """Trouve les articles pertinents selon le type de prime"""
    relevant_articles = []
    
    # Mappage intelligent basé sur les mots-clés du type de prime
    keywords_mapping = {
        "rendement": ["Art.L.30", "Art.L.31", "Art.L.32"],  # Contrats et rémunération
        "ancienneté": ["Art.L.42", "Art.L.43", "Art.L.47"],  # Durée et fin de contrat
        "risque": ["Art.L.4", "Art.L.35"],  # Conditions de travail
        "résultat": ["Art.L.30", "Art.L.31", "Art.L.35"],  # Performance et rémunération
        "assiduité": ["Art.L.35", "Art.L.50"],  # Présence et discipline
        "fin": ["Art.L.47", "Art.L.48"],  # Fin de contrat et indemnités
        "transport": ["Art.L.33", "Art.L.34"]  # Déplacements et conditions
    }
    
    # Recherche par mots-clés
    for keyword, articles in keywords_mapping.items():
        if keyword.lower() in prime_type.lower():
            relevant_articles.extend(articles)
    
    # Articles généraux applicables à toutes les primes
    general_articles = ["Art.L.2", "Art.L.3", "Art.L.30", "Art.L.31", "Art.L.35"]
    relevant_articles.extend(general_articles)
    
    # Supprimer les doublons et retourner
    return list(set(relevant_articles))

def generate_explanations_from_articles(articles: List[str]) -> List[str]:
    """Génère des explications basées sur le contenu des articles"""
    explanations = []
    code_articles = load_articles_from_postgres()
    
    for article_code in articles:
        if article_code in code_articles:
            content = code_articles[article_code]
            # Extraire les points clés du contenu
            key_points = []
            
            # Chercher des phrases importantes
            sentences = content.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20:  # Phrases substantielles
                    # Nettoyer et raccourcir
                    clean_sentence = sentence.replace(',,', '').strip()
                    if len(clean_sentence) > 10:
                        key_points.append(clean_sentence[:150] + "..." if len(clean_sentence) > 150 else clean_sentence)
            
            # Ajouter les 2 premiers points les plus pertinents
            explanations.extend(key_points[:2])
    
    # Limiter à 5 explications maximum
    return explanations[:5] if explanations else ["Dispositions générales du Code du travail Sénégalais"]

def get_article_by_code(article_code: str) -> Optional[str]:
    """Récupère le contenu d'un article par son code depuis PostgreSQL"""
    articles = load_articles_from_postgres()
    return articles.get(article_code)

def search_articles_by_keyword(keyword: str) -> List[dict]:
    """Recherche des articles par mot-clé dans PostgreSQL"""
    results = []
    
    if not PSYCOPG2_AVAILABLE:
        return results
    
    keyword_lower = keyword.lower()
    
    connection = get_db_connection()
    if not connection:
        return results
    
    try:
        if not PSYCOPG2_AVAILABLE:
            return results
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT article_code, contenu FROM public.articles WHERE LOWER(contenu) LIKE %s",
            (f"%{keyword_lower}%",)
        )
        
        for row in cursor.fetchall():
            article_code = row['article_code']
            content = row['contenu']
            
            # Extraire un extrait autour du mot-clé
            content_lower = content.lower()
            index = content_lower.find(keyword_lower)
            if index != -1:
                start = max(0, index - 100)
                end = min(len(content), index + len(keyword) + 100)
                excerpt = content[start:end]
                
                results.append({
                    "article": article_code,
                    "extrait": excerpt,
                    "position": index
                })
    
    except Exception as e:
        print(f"Erreur lors de la recherche: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    
    return results[:10]  # Limiter à 10 résultats

def get_articles_count() -> int:
    """Retourne le nombre d'articles dans la table PostgreSQL"""
    if not PSYCOPG2_AVAILABLE:
        return 0
    
    connection = get_db_connection()
    if not connection:
        return 0
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM public.articles")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print(f"Erreur lors du comptage des articles: {e}")
        return 0
    finally:
        if connection:
            cursor.close()
            connection.close()

# Base de données simulée pour les primes (peut être migrée vers PostgreSQL plus tard)
primes_db = []

def add_prime_to_db(prime_data: dict) -> None:
    """Ajoute une prime à la base de données (pour l'instant en mémoire)"""
    primes_db.append(prime_data)

def get_prime_by_id(prime_id: int) -> Optional[dict]:
    """Récupère une prime par son ID"""
    if prime_id < 0 or prime_id >= len(primes_db):
        return None
    return primes_db[prime_id]

def get_all_primes() -> List[dict]:
    """Récupère toutes les primes"""
    return primes_db

def get_primes_by_type(type_prime: str) -> List[dict]:
    """Récupère toutes les primes d'un type spécifique"""
    return [prime for prime in primes_db if prime["type_prime"] == type_prime]

def get_available_prime_types() -> List[str]:
    """Récupère tous les types de primes disponibles"""
    return list(set([prime["type_prime"] for prime in primes_db]))

# Chargement initial des articles depuis PostgreSQL
# Chargement lazy pour éviter les problèmes au démarrage sur Netlify
code_articles = {}
try:
    import sys
    if sys.stdout.encoding and 'utf' in sys.stdout.encoding.lower():
        print("🔄 Chargement des articles depuis PostgreSQL...")
    else:
        print("Chargement des articles depuis PostgreSQL...")
    code_articles = load_articles_from_postgres()
except Exception as e:
    print(f"⚠️ Erreur lors du chargement initial des articles: {e}")
    print("Les articles seront chargés à la demande")
    code_articles = {}
