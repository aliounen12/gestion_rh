#!/usr/bin/env python3
"""
Test pour vérifier que les articles sont bien inclus dans le prompt
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.tools import extract_keywords, create_system_prompt
from app.db import get_all_sujets, get_articles_by_sujet

# Simuler une question sur les congés
message = "Quels sont les droits des travailleurs concernant les congés ?"

print("=" * 60)
print("TEST: Inclusion des articles dans le prompt")
print("=" * 60)

# 1. Extraire les mots-clés
keywords = extract_keywords(message)
print(f"\n1. Mots-clés extraits: {keywords}")

# 2. Trouver le sujet correspondant
sujets = get_all_sujets()
sujet_trouve = None

for keyword in keywords:
    for sujet in sujets:
        if keyword.lower() in sujet['titre_sujet'].lower() or str(sujet['id']) == keyword:
            sujet_trouve = sujet
            break
    if sujet_trouve:
        break

# 3. Récupérer les articles
if sujet_trouve:
    print(f"\n2. Sujet trouvé: {sujet_trouve['titre_sujet']} (ID: {sujet_trouve['id']})")
    articles = get_articles_by_sujet(sujet_trouve['id'])
    print(f"   ✅ {len(articles)} articles récupérés")
    
    # 4. Créer le prompt système
    system_prompt = create_system_prompt("", articles)
    
    print(f"\n3. Prompt système généré ({len(system_prompt)} caractères)")
    print("\n" + "=" * 60)
    print("EXTRAIT DU PROMPT (premiers 500 caractères):")
    print("=" * 60)
    print(system_prompt[:500])
    print("\n...")
    print("\n" + "=" * 60)
    print("EXTRAIT DU PROMPT (derniers 500 caractères):")
    print("=" * 60)
    print(system_prompt[-500:])
    
    # Vérifier que les articles sont inclus
    if "ARTICLES DU CODE DU TRAVAIL" in system_prompt:
        print("\n✅ Les articles sont bien inclus dans le prompt système !")
    else:
        print("\n❌ Les articles ne sont PAS inclus dans le prompt système !")
    
    # Compter les articles dans le prompt
    article_count = system_prompt.count("Article")
    print(f"✅ {article_count} articles détectés dans le prompt")
else:
    print("\n❌ Aucun sujet trouvé pour les mots-clés")

print("\n" + "=" * 60)
