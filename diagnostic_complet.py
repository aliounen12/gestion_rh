#!/usr/bin/env python3
"""
Script de diagnostic complet pour identifier tous les problèmes
"""

def diagnostic_complet():
    print("🔍 DIAGNOSTIC COMPLET DE L'API")
    print("=" * 60)
    
    # 1. Connectivité réseau
    print("\n1. 🌐 Test de connectivité...")
    try:
        import requests
        response = requests.get("http://localhost:8000/test", timeout=5)
        if response.status_code == 200:
            print("✅ API accessible sur localhost:8000")
            data = response.json()
            print(f"   Articles chargés: {data.get('articles_charges', 'N/A')}")
            print(f"   Primes enregistrées: {data.get('primes_enregistrees', 'N/A')}")
        else:
            print(f"❌ API répond avec code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ API non accessible - elle n'est probablement pas démarrée")
    except ImportError:
        print("⚠️  Module 'requests' non disponible")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # 2. Test des endpoints
    print("\n2. 📊 Test des endpoints...")
    endpoints_a_tester = [
        "/test",
        "/primes/",
        "/types-primes/",
        "/primes/par-type/Prime%20de%20risque"
    ]
    
    for endpoint in endpoints_a_tester:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint}: OK")
            elif response.status_code == 404:
                print(f"⚠️  {endpoint}: 404 (normal si pas de données)")
            else:
                print(f"❌ {endpoint}: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   Détail: {error_detail}")
                except:
                    print(f"   Détail: {response.text[:100]}")
        except Exception as e:
            print(f"❌ {endpoint}: Erreur - {e}")
    
    # 3. Test de création de primes
    print("\n3. 📝 Test de création de primes...")
    try:
        # Test avec l'endpoint de création d'exemples
        response = requests.post("http://localhost:8000/primes/creer-exemples", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Création d'exemples réussie: {data.get('message', 'N/A')}")
            print(f"   Total primes: {data.get('total_primes', 'N/A')}")
        else:
            print(f"❌ Erreur création exemples: {response.status_code}")
            print(f"   Détail: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Erreur création primes: {e}")
    
    # 4. Test après création
    print("\n4. 🔄 Test après création...")
    try:
        # Vérifier les types disponibles
        response = requests.get("http://localhost:8000/types-primes/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Types disponibles: {data.get('nombre_types', 0)}")
            for type_prime in data.get('types_primes_disponibles', [])[:3]:
                print(f"   - {type_prime}")
        
        # Test d'un type spécifique
        response = requests.get("http://localhost:8000/primes/par-type/Prime%20de%20risque", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prime de risque trouvée: {data.get('nombre_primes', 0)} prime(s)")
        elif response.status_code == 404:
            print("⚠️  Prime de risque non trouvée (404)")
        else:
            print(f"❌ Erreur prime de risque: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur test final: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 60)
    print("Si vous voyez des ❌, voici les solutions:")
    print("1. API non accessible → python main.py")
    print("2. Pas de primes → Utilisez l'interface web pour créer des primes")
    print("3. Erreurs 404 → Normal si pas de données, créez des primes d'abord")
    print("4. Erreurs Python → Installez Python et les dépendances")

if __name__ == "__main__":
    diagnostic_complet()
