#!/usr/bin/env python3
"""
Fonctions d'aide pour la gestion RH
"""

from typing import Dict, List, Optional

def get_rh_context(topic: Optional[str] = None) -> str:
    """
    Retourne le contexte RH selon le sujet depuis PostgreSQL
    
    Args:
        topic: Le sujet de la question (peut être un ID de sujet ou un mot-clé)
    
    Returns:
        Le contexte RH formaté avec les données de la base
    """
    try:
        from app.db import get_all_sujets, get_sujet_by_id, get_articles_by_sujet
        
        # Récupérer tous les sujets disponibles
        sujets = get_all_sujets()
        
        if not sujets:
            # Fallback si PostgreSQL n'est pas disponible
            return """
Domaines d'expertise:
- Gestion des primes et avantages
- Droit du travail
- Conformité légale
- Relations de travail
- Gestion des performances
- Formation et développement
"""
        
        # Construire le contexte avec les sujets de la base
        context = "Domaines d'expertise disponibles dans la base de données:\n"
        for sujet in sujets:
            context += f"- {sujet['titre_sujet']}: {sujet['description']}\n"
        
        # Si un topic spécifique est fourni, essayer de trouver le sujet correspondant
        if topic:
            # Essayer de trouver par ID
            try:
                sujet_id = int(topic)
                sujet = get_sujet_by_id(sujet_id)
                if sujet:
                    articles = get_articles_by_sujet(sujet_id)
                    context += f"\nFocus sur: {sujet['titre_sujet']}\n"
                    context += f"Description: {sujet['description']}\n"
                    context += f"Nombre d'articles disponibles: {len(articles)}\n"
                    return context
            except ValueError:
                pass
            
            # Chercher par titre de sujet
            topic_lower = topic.lower()
            for sujet in sujets:
                if topic_lower in sujet['titre_sujet'].lower():
                    articles = get_articles_by_sujet(sujet['id'])
                    context += f"\nFocus sur: {sujet['titre_sujet']}\n"
                    context += f"Description: {sujet['description']}\n"
                    context += f"Nombre d'articles disponibles: {len(articles)}\n"
                    return context
        
        return context
    
    except Exception as e:
        print(f"Erreur lors de la récupération du contexte RH: {e}")
        # Fallback
        return """
Domaines d'expertise:
- Gestion des primes et avantages
- Droit du travail
- Conformité légale
- Relations de travail
- Gestion des performances
- Formation et développement
"""

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
    Extrait les mots-clés d'un message pour identifier le sujet depuis PostgreSQL
    
    Args:
        message: Le message à analyser
    
    Returns:
        Une liste de mots-clés identifiés (titres de sujets ou catégories)
    """
    keywords = []
    message_lower = message.lower()
    
    # Mapping des mots-clés vers les titres de sujets (utilisé même si PostgreSQL n'est pas disponible)
    keyword_to_sujet = {
        "congé": "Congés",
        "congés": "Congés", 
        "vacances": "Congés",
        "repos": "Congés",
        "transport": "Transport",
        "tansport": "Transport",  # Typo possible
        "déplacement": "Transport",
        "frais": "Transport",
        "trajet": "Transport"
    }
    
    # D'abord, chercher les mots-clés connus dans le message
    for keyword, sujet_titre in keyword_to_sujet.items():
        # Normaliser pour gérer les accents
        keyword_normalized = keyword.lower().replace('é', 'e').replace('è', 'e').replace('ê', 'e')
        message_normalized = message_lower.replace('é', 'e').replace('è', 'e').replace('ê', 'e')
        
        if keyword in message_lower or keyword_normalized in message_normalized:
            keywords.append(sujet_titre)
            # Si PostgreSQL est disponible, récupérer l'ID
            try:
                from app.db import get_all_sujets
                sujets = get_all_sujets()
                for sujet in sujets:
                    if sujet['titre_sujet'] == sujet_titre:
                        keywords.append(str(sujet['id']))
                        break
            except:
                pass
            break  # Un seul sujet à la fois
    
    # Si pas de mot-clé trouvé, chercher dans PostgreSQL
    if not keywords:
        try:
            from app.db import get_all_sujets
            
            # Récupérer les sujets depuis la base de données
            sujets = get_all_sujets()
            
            # Chercher les correspondances avec les titres de sujets
            for sujet in sujets:
                titre_lower = sujet['titre_sujet'].lower()
                # Vérifier si le titre du sujet est dans le message
                if titre_lower in message_lower:
                    keywords.append(sujet['titre_sujet'])
                    keywords.append(str(sujet['id']))  # Ajouter aussi l'ID
                # Vérifier si des mots du titre sont dans le message
                elif any(word in message_lower for word in titre_lower.split() if len(word) > 3):
                    keywords.append(sujet['titre_sujet'])
                    keywords.append(str(sujet['id']))
                # Vérifier si des mots du message sont dans le titre
                elif any(word in titre_lower for word in message_lower.split() if len(word) > 3):
                    keywords.append(sujet['titre_sujet'])
                    keywords.append(str(sujet['id']))
            
            # Si toujours rien, utiliser les mots-clés génériques
            if not keywords:
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
        except Exception as e:
            print(f"Erreur lors de l'extraction des mots-clés: {e}")
            # Fallback vers les mots-clés par défaut
            if not keywords:
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
