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
    # Identifiant OpenRouter au format fournisseur/nom, ex. openai/gpt-4o-mini
    OPENROUTER_MODEL = (os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini") or "").strip()
    OPENROUTER_MODEL_FALLBACK = (
        os.getenv("OPENROUTER_MODEL_FALLBACK", "openai/gpt-4o-mini") or ""
    ).strip()
    OPENROUTER_MAX_TOKENS = int(os.getenv("OPENROUTER_MAX_TOKENS", "1000"))
    OPENROUTER_TEMPERATURE = float(os.getenv("OPENROUTER_TEMPERATURE", "0.7"))
    # Limite totale (caractères) prompt système + message user — évite le HTTP 400 « context length »
    OPENROUTER_MAX_TOTAL_PROMPT_CHARS = int(os.getenv("OPENROUTER_MAX_TOTAL_PROMPT_CHARS", "85000"))
    # Budget tokens approximatif réservé à l'entrée (reste = marge pour max_tokens de sortie)
    OPENROUTER_INPUT_TOKEN_BUDGET = int(os.getenv("OPENROUTER_INPUT_TOKEN_BUDGET", "12000"))

    # Chat : taille du contexte Code du travail envoyé au LLM
    CHAT_MAX_ARTICLES = int(os.getenv("CHAT_MAX_ARTICLES", "8"))
    CHAT_MAX_CHARS_PER_ARTICLE = int(os.getenv("CHAT_MAX_CHARS_PER_ARTICLE", "4500"))
    
    # Base de données (optionnel)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "chatrh_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    # Source de données (fichier) - Code du travail DOCX
    # Par défaut: fichier `Code_du_travail_SN` à la racine du projet
    CODE_TRAVAIL_PATH = os.getenv("CODE_TRAVAIL_PATH", "")

# Instance globale des paramètres
settings = Settings()
