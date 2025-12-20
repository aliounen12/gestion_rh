"""
Netlify Function handler pour l'API FastAPI
Optimisé pour Netlify Functions
"""

import sys
import os
import json

# Configuration du path Python pour Netlify
# Dans Netlify Functions, le répertoire de travail est différent
current_file = os.path.abspath(__file__)
functions_dir = os.path.dirname(current_file)
netlify_dir = os.path.dirname(functions_dir)
root_dir = os.path.dirname(netlify_dir)

# Ajouter le répertoire racine au path
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Essayer de changer le répertoire de travail (optionnel)
try:
    os.chdir(root_dir)
except:
    pass

# Import de l'application FastAPI avec gestion d'erreurs
mangum_handler = None
app = None
import_error = None

try:
    from mangum import Mangum
    from app.main import app
    
    if app is not None:
        # Créer le handler Mangum pour Netlify
        # lifespan="off" car Netlify Functions ne supporte pas les événements de lifespan
        mangum_handler = Mangum(app, lifespan="off", api_gateway_base_path="")
except Exception as e:
    import_error = str(e)
    print(f"Erreur lors de l'import: {e}")
    import traceback
    traceback.print_exc()

def handler(event, context):
    """
    Handler principal pour Netlify Functions
    
    Args:
        event: Événement Netlify Function (dict)
        context: Contexte de la fonction
    
    Returns:
        Réponse HTTP (dict)
    """
    # Vérifier si le handler est initialisé
    if mangum_handler is None:
        error_msg = {
            'error': 'Handler not initialized',
            'message': 'Erreur lors de l\'initialisation de l\'application',
            'import_error': import_error if import_error else 'Unknown error'
        }
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(error_msg)
        }
    
    try:
        # Netlify Functions passe l'événement directement à Mangum
        # Mangum gère la conversion du format Netlify vers ASGI
        response = mangum_handler(event, context)
        
        # S'assurer que la réponse a le bon format
        if isinstance(response, dict):
            # Ajouter CORS headers si pas déjà présents
            if 'headers' in response:
                response['headers'].setdefault('Access-Control-Allow-Origin', '*')
            else:
                response['headers'] = {'Access-Control-Allow-Origin': '*'}
        
        return response
    except Exception as e:
        print(f"Erreur dans le handler: {e}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Erreur lors du traitement de la requête',
                'type': type(e).__name__
            })
        }
