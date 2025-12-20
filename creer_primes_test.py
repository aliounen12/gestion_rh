#!/usr/bin/env python3
"""
Script pour créer des primes d'exemple et tester l'API
"""

import requests
import json

def creer_primes_exemples():
    print("🚀 Création de primes d'exemple pour tester l'API...")
    print("=" * 60)
    
    # URL de l'API (assume qu'elle tourne sur localhost:8000)
    base_url = "http://localhost:8000"
    
    try:
        # 1. Vérifier que l'API fonctionne
        print("🔍 Vérification de l'API...")
        response = requests.get(f"{base_url}/test")
        if response.status_code == 200:
            print("✅ API fonctionnelle")
            data = response.json()
            print(f"   Articles chargés: {data['articles_charges']}")
            print(f"   Primes enregistrées: {data['primes_enregistrees']}")
        else:
            print("❌ API non accessible")
            return
        
        # 2. Créer des primes d'exemple
        print("\n📝 Création de primes d'exemple...")
        response = requests.post(f"{base_url}/primes/creer-exemples")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
            print(f"   Total primes: {data['total_primes']}")
            
            # Afficher les primes créées
            print("\n📋 Primes créées:")
            for prime in data['primes_creees']:
                print(f"   - {prime['type_prime']}: {prime['motif']}")
        else:
            print(f"❌ Erreur création primes: {response.status_code}")
            print(response.text)
            return
        
        # 3. Tester la récupération par type
        print("\n🔍 Test de récupération par type...")
        types_a_tester = [
            "Prime de rendement",
            "Prime de risque", 
            "Prime d'ancienneté"
        ]
        
        for type_prime in types_a_tester:
            # Encoder l'URL pour les espaces
            type_encoded = type_prime.replace(" ", "%20")
            response = requests.get(f"{base_url}/primes/par-type/{type_encoded}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {type_prime}: {data['nombre_primes']} prime(s)")
            else:
                print(f"❌ {type_prime}: Erreur {response.status_code}")
        
        # 4. Afficher tous les types disponibles
        print("\n📊 Types de primes disponibles:")
        response = requests.get(f"{base_url}/types-primes/")
        if response.status_code == 200:
            data = response.json()
            print(f"   Nombre de types: {data['nombre_types']}")
            for type_prime in data['types_primes_disponibles']:
                print(f"   - {type_prime}")
        
        print("\n🎉 Tests terminés avec succès!")
        print("🌐 Vous pouvez maintenant tester l'API avec des données")
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API")
        print("💡 Assurez-vous que l'API est démarrée avec: python main.py")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    creer_primes_exemples()
