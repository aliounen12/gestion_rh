#!/usr/bin/env python3
"""
Point d'entrée principal pour le développement local
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    from app.config import settings
    
    print("🚀 Démarrage de l'API ChatRH")
    print(f"🌐 Serveur disponible sur: http://localhost:{settings.API_PORT}")
    print("📖 Documentation: http://localhost:8000/docs")
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
