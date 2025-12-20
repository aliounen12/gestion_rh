#!/usr/bin/env python3
"""
Point d'entrée principal de l'application
Redirige vers app.main pour faciliter le démarrage
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    from app.config import settings
    from app.db import code_articles
    
    print("🚀 Démarrage de l'API Gestion des Primes")
    print(f"🗄️  Base de données: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    print(f"📚 Articles chargés depuis PostgreSQL: {len(code_articles)}")
    print("🌐 Serveur disponible sur: http://localhost:8000")
    print("📖 Documentation: http://localhost:8000/docs")
    print("🧪 Test API: http://localhost:8000/test")
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
