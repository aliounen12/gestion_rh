"""
Netlify Function handler pour l'API FastAPI
"""

import sys
import os
import json

# Ajouter le répertoire racine au path Python
# Dans Netlify, le répertoire de travail est différent
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '../../'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# S'assurer que le répertoire de travail est correct
try:
    os.chdir(root_dir)
except:
    pass  # Si on ne peut pas changer, continuer quand même

try:
    from mangum import Mangum
    from app.main import app
    
    # Créer le handler Mangum pour Netlify
    # lifespan="off" car Netlify Functions ne supporte pas les événements de lifespan
    mangum_handler = Mangum(app, lifespan="off")
except Exception as e:
    # En cas d'erreur d'import, créer un handler d'erreur
    print(f"Erreur lors de l'import: {e}")
    mangum_handler = None
    app = None

def handler(event, context):
    """
    Handler principal pour Netlify Functions
    
    Args:
        event: Événement Netlify Function (dict)
        context: Contexte de la fonction
    
    Returns:
        Réponse HTTP (dict)
    """
    if mangum_handler is None:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Handler not initialized',
                'message': 'Erreur lors de l\'initialisation de l\'application'
            })
        }
    
    try:
        # Convertir l'événement Netlify en format Mangum
        # Netlify Functions Python passe l'événement comme un dict
        response = mangum_handler(event, context)
        return response
    except Exception as e:
        print(f"Erreur dans le handler: {e}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': str(e),
                'message': 'Erreur lors du traitement de la requête'
            })
        }
