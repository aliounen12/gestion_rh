import sys
import os

# Ajouter le répertoire parent au path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Importer l'application FastAPI
from app.main import app

# Vercel détecte automatiquement 'app' comme application ASGI
# L'app FastAPI est directement exportée

