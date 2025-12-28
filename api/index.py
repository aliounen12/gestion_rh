#!/usr/bin/env python3
"""
Handler Vercel pour ChatRH API
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from mangum import Mangum
    from app.main import app
    
    # Créer le handler Mangum pour Vercel
    handler = Mangum(app, api_gateway_base_path="")
    
except Exception as e:
    # Handler d'erreur en cas d'échec d'import
    def handler(event, context):
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": f'{{"error": "Erreur d\'initialisation", "detail": "{str(e)}"}}'
        }
