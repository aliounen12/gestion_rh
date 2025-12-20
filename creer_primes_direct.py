#!/usr/bin/env python3
"""
Script pour créer des primes d'exemple directement dans la base de données
"""

def creer_primes_directement():
    print("🚀 Création directe de primes d'exemple...")
    print("=" * 50)
    
    try:
        # Import des fonctions nécessaires
        from app.db import add_prime_to_db, get_all_primes, find_relevant_articles, generate_explanations_from_articles
        from app.models import Prime
        
        # Types de primes à créer
        types_primes_exemples = [
            ("Prime de rendement", "Prime pour excellentes performances"),
            ("Prime de risque", "Prime pour travail en conditions dangereuses"),
            ("Prime d'ancienneté", "Prime pour 5 ans d'ancienneté"),
            ("Prime de résultat", "Prime pour objectifs atteints"),
            ("Prime d'assiduité", "Prime pour parfaite assiduité"),
            ("Prime de fin d'année", "Prime de fin d'année 2024"),
            ("Prime de transport", "Prime pour frais de transport")
        ]
        
        primes_creees = []
        
        for type_prime, motif in types_primes_exemples:
            print(f"📝 Création de: {type_prime}")
            
            # Créer la prime
            prime = Prime(type_prime=type_prime, motif=motif)
            
            # Déterminer les articles de conformité
            articles = find_relevant_articles(prime.type_prime)
            explications = generate_explanations_from_articles(articles)
            
            prime.conformite = {
                "articles": articles,
                "explications": explications
            }
            
            # Ajouter à la base de données
            add_prime_to_db(prime.dict())
            primes_creees.append({
                "type_prime": type_prime,
                "motif": motif,
                "articles_conformite": len(articles)
            })
            
            print(f"   ✅ Créée avec {len(articles)} articles de conformité")
        
        # Vérification finale
        total_primes = len(get_all_primes())
        print(f"\n🎉 {len(primes_creees)} primes créées avec succès!")
        print(f"📊 Total primes en base: {total_primes}")
        
        # Afficher un résumé
        print("\n📋 Résumé des primes créées:")
        for prime in primes_creees:
            print(f"   - {prime['type_prime']}: {prime['motif']}")
        
        print("\n🌐 Vous pouvez maintenant tester l'API:")
        print("   - GET /primes/par-type/Prime%20de%20risque")
        print("   - GET /types-primes/")
        print("   - GET /primes/")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    creer_primes_directement()
