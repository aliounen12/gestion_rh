"""
Handler Vercel pour ChatRH API
Vercel s'attend à une variable 'handler' qui pointe vers l'application ASGI
"""
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer l'application FastAPI
from app.main import app

# Vercel s'attend à une variable 'handler' qui pointe vers l'app ASGI
handler = app

