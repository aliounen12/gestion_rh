#!/usr/bin/env python3
"""
Script de test pour vérifier la source de données (DOCX) et la récupération des articles
"""

import sys
import os

# Ajouter le répertoire au path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app.db import (
        get_all_sujets,
        get_articles_by_sujet,
        get_articles_count,
        search_articles
    )
    from app.tools import extract_keywords
    
    print("=" * 60)
    print("TEST SOURCE DE DONNÉES (DOCX)")
    print("=" * 60)
    
    # Test 1: Récupérer tous les sujets
    print("\n1. Test: Récupération des sujets...")
    sujets = get_all_sujets()
    print(f"   OK: {len(sujets)} sujets trouvés:")
    for sujet in sujets:
        print(f"      - {sujet['titre_sujet']} (ID: {sujet['id']})")
        print(f"        Description: {sujet['description'][:60]}...")
    
    # Test 2: Récupérer les articles d'un sujet
    if sujets:
        print(f"\n2. Test: Articles du sujet '{sujets[0]['titre_sujet']}' (ID: {sujets[0]['id']})...")
        articles = get_articles_by_sujet(sujets[0]['id'])
        print(f"   OK: {len(articles)} articles trouvés")
        for i, article in enumerate(articles[:3], 1):
            print(f"      Article {i}: {article['num_article']}")
            print(f"        Source: {article['source']}")
            print(f"        Contenu: {article['contenu'][:80]}...")
    
    # Test 3: Nombre total d'articles
    print("\n3. Test: Nombre total d'articles...")
    count = get_articles_count()
    print(f"   OK: {count} articles au total dans la source")
    
    # Test 4: Recherche d'articles
    print("\n4. Test: Recherche d'articles avec le mot 'congé'...")
    articles = search_articles("congé", limit=3)
    print(f"   OK: {len(articles)} articles trouvés")
    for article in articles:
        print(f"      - {article['num_article']}: {article['contenu'][:60]}...")
    
    # Test 5: Extraction de mots-clés
    print("\n5. Test: Extraction de mots-clés...")
    message = "Quels sont les droits des travailleurs concernant les congés ?"
    keywords = extract_keywords(message)
    print(f"   Message: {message}")
    print(f"   OK: Mots-clés détectés: {keywords}")
    
    # Test 6: Recherche pour "congés"
    if "Congés" in keywords or any("congé" in k.lower() for k in keywords):
        print("\n6. Test: Récupération des articles sur les congés...")
        for sujet in sujets:
            if "Congés" in sujet['titre_sujet']:
                articles = get_articles_by_sujet(sujet['id'])
                print(f"   OK: {len(articles)} articles sur les congés trouvés")
                break
    
    print("\n" + "=" * 60)
    print("OK: TOUS LES TESTS RÉUSSIS - La source de données fonctionne !")
    print("=" * 60)
    
except Exception as e:
    print(f"\nERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
