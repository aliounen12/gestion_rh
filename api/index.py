#!/usr/bin/env python3
"""
Handler Vercel pour ChatRH API
Vercel supporte nativement les applications ASGI (FastAPI/Starlette)
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

# Vercel supporte nativement ASGI, on exporte directement l'app FastAPI
# Pas besoin de Mangum pour Vercel

