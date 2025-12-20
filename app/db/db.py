#!/usr/bin/env python3
"""
Gestion de la base de données et des données
"""

import csv
from typing import Dict, List

# Base de données simulée
primes_db = []

def load_articles_from_csv() -> Dict[str, str]:
    """Charge les articles du Code du travail depuis le fichier CSV"""
    articles = {}
    try:
        with open('articles_structures.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                article_code = row['Article']
                content = row['Contenu']
                # Nettoyer le contenu des caractères d'encodage problématiques
                content = content.replace('ï¿½', 'é').replace('Ã¯Â¿Â½', 'é')
                articles[article_code] = content
    except FileNotFoundError:
        print("Fichier articles_structures.csv non trouvé")
    except Exception as e:
        print(f"Erreur lors du chargement du CSV: {e}")
    return articles

# Chargement des articles au démarrage
code_articles = load_articles_from_csv()

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

def add_prime_to_db(prime_data: dict) -> None:
    """Ajoute une prime à la base de données"""
    primes_db.append(prime_data)

def get_prime_by_id(prime_id: int) -> dict:
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

def get_article_by_code(article_code: str) -> str:
    """Récupère le contenu d'un article par son code"""
    return code_articles.get(article_code)

def search_articles_by_keyword(keyword: str) -> List[dict]:
    """Recherche des articles par mot-clé"""
    results = []
    keyword_lower = keyword.lower()
    
    for article_code, content in code_articles.items():
        if keyword_lower in content.lower():
            # Extraire un extrait autour du mot-clé
            content_lower = content.lower()
            index = content_lower.find(keyword_lower)
            start = max(0, index - 100)
            end = min(len(content), index + len(keyword) + 100)
            excerpt = content[start:end]
            
            results.append({
                "article": article_code,
                "extrait": excerpt,
                "position": index
            })
    
    return results[:10]  # Limiter à 10 résultats
