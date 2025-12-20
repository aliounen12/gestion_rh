"""
Netlify Function handler pour l'API FastAPI
"""

import sys
import os

# Ajouter le répertoire racine au path Python
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, root_dir)

# S'assurer que le répertoire de travail est correct
os.chdir(root_dir)

from mangum import Mangum
from app.main import app

# Créer le handler Mangum pour Netlify
# lifespan="off" car Netlify Functions ne supporte pas les événements de lifespan
mangum_handler = Mangum(app, lifespan="off")

def handler(event, context):
    """
    Handler principal pour Netlify Functions
    
    Args:
        event: Événement Netlify Function
        context: Contexte de la fonction
    
    Returns:
        Réponse HTTP
    """
    return mangum_handler(event, context)
