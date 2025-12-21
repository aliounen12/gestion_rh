#!/usr/bin/env python3
"""
Configuration de l'application ChatRH
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Settings:
    """Configuration de l'application"""
    
    # Configuration API
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Configuration OpenRouter (optionnel)
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
    OPENROUTER_MAX_TOKENS = int(os.getenv("OPENROUTER_MAX_TOKENS", "1000"))
    OPENROUTER_TEMPERATURE = float(os.getenv("OPENROUTER_TEMPERATURE", "0.7"))
    
    # Base de données (optionnel)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "chatrh_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Instance globale des paramètres
settings = Settings()
