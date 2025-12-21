#!/usr/bin/env python3
"""
Fonctions d'aide pour la gestion RH
"""

from typing import Dict, List, Optional

def get_rh_context(topic: Optional[str] = None) -> str:
    """
    Retourne le contexte RH selon le sujet
    
    Args:
        topic: Le sujet de la question
    
    Returns:
        Le contexte RH formaté
    """
    base_context = """
Domaines d'expertise:
- Gestion des primes et avantages
- Droit du travail
- Conformité légale
- Relations de travail
- Gestion des performances
- Formation et développement
"""
    
    topic_contexts = {
        "prime": "Focus sur les primes: types de primes, calcul, conformité légale",
        "droit": "Focus sur le droit du travail: contrats, conventions, obligations",
        "performance": "Focus sur la gestion des performances: évaluation, objectifs, feedback",
        "formation": "Focus sur la formation: développement des compétences, planification"
    }
    
    if topic and topic.lower() in topic_contexts:
        return base_context + f"\n{topic_contexts[topic.lower()]}"
    
    return base_context

def format_rh_advice(advice: str, category: Optional[str] = None) -> Dict[str, str]:
    """
    Formate un conseil RH avec métadonnées
    
    Args:
        advice: Le conseil à formater
        category: La catégorie du conseil (prime, droit, performance, etc.)
    
    Returns:
        Un dictionnaire avec le conseil formaté et ses métadonnées
    """
    formatted = {
        "advice": advice,
        "category": category or "general",
        "source": "ChatRH Assistant"
    }
    
    return formatted

def extract_keywords(message: str) -> List[str]:
    """
    Extrait les mots-clés d'un message pour identifier le sujet
    
    Args:
        message: Le message à analyser
    
    Returns:
        Une liste de mots-clés identifiés
    """
    keywords = []
    message_lower = message.lower()
    
    # Mots-clés RH
    rh_keywords = {
        "prime": ["prime", "primes", "bonus", "gratification"],
        "droit": ["droit", "loi", "code", "légal", "conformité"],
        "performance": ["performance", "évaluation", "objectif", "résultat"],
        "formation": ["formation", "apprentissage", "compétence", "développement"],
        "contrat": ["contrat", "embauche", "recrutement", "candidat"]
    }
    
    for category, words in rh_keywords.items():
        if any(word in message_lower for word in words):
            keywords.append(category)
    
    return keywords
