from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api import assistant_router, health_router
from app.config import settings

app = FastAPI(
    title="Gestion RH Assistant",
    description="API simplifiée avec assistant IA pour la gestion des ressources humaines",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP
    allow_headers=["*"],  # Autorise tous les headers
)

# Inclusion des routers - API simplifiée avec 3 endpoints seulement
app.include_router(assistant_router)
app.include_router(health_router)


# Démarrage automatique du serveur
if __name__ == "__main__":
    from app.db import code_articles
    print("🚀 Démarrage de l'API Gestion RH Assistant")
    print(f"🗄️  Base de données: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    print(f"📚 Articles chargés depuis PostgreSQL: {len(code_articles)}")
    print("🌐 Serveur disponible sur: http://localhost:8000")
    print("📖 Documentation: http://localhost:8000/docs")
    print("✅ Endpoints disponibles:")
    print("   - POST /assistant/chat")
    print("   - GET /assistant/tools")
    print("   - GET /gestionrh")
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )