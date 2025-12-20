#!/usr/bin/env python3
"""
Script de test pour vérifier que le handler Netlify fonctionne
"""

def test_handler():
    """Test le handler Netlify localement"""
    print("🧪 Test du handler Netlify...")
    
    try:
        # Simuler un événement Netlify
        event = {
            'httpMethod': 'GET',
            'path': '/gestionrh',
            'headers': {},
            'queryStringParameters': None,
            'body': None,
            'isBase64Encoded': False
        }
        
        context = {}
        
        # Importer et tester le handler
        import sys
        import os
        sys.path.insert(0, os.path.dirname(__file__))
        
        from netlify.functions.api import handler
        
        print("✅ Handler importé avec succès")
        
        # Tester le handler
        response = handler(event, context)
        
        print(f"✅ Handler exécuté avec succès")
        print(f"Status Code: {response.get('statusCode', 'N/A')}")
        print(f"Response: {response.get('body', 'N/A')[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_handler()
    if success:
        print("\n✅ Test réussi ! Le handler devrait fonctionner sur Netlify")
    else:
        print("\n❌ Test échoué ! Vérifiez les erreurs ci-dessus")
