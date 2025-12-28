"""
Handler Vercel pour ChatRH API
"""
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path Python
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

# Importer l'application FastAPI
from app.main import app

# Vercel cherche une variable 'handler' qui pointe vers l'app ASGI
handler = app

