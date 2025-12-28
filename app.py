"""
Point d'entrée principal pour Vercel
"""
import sys
from pathlib import Path

# Ajouter le répertoire courant au path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Importer l'application FastAPI
from app.main import app

# Vercel cherche une variable 'app' ou 'handler'
# On exporte les deux pour être sûr
handler = app
