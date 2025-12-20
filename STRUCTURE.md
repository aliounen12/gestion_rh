# 📁 Structure du Projet

## Architecture

Le projet est maintenant organisé selon une architecture modulaire claire :

```
gestion_rh/
├── app/                          # Package principal de l'application
│   ├── __init__.py              # Initialisation du package
│   ├── main.py                   # Point d'entrée FastAPI
│   ├── config.py                 # Configuration de l'application
│   │
│   ├── api/                      # Module API - Routers FastAPI
│   │   ├── __init__.py
│   │   └── routers.py            # Tous les endpoints de l'API
│   │
│   ├── db/                       # Module DB - Gestion de la base de données
│   │   ├── __init__.py
│   │   ├── db_postgres.py        # Fonctions PostgreSQL
│   │   └── db.py                 # Fonctions de base de données
│   │
│   ├── llm/                      # Module LLM - Intégration OpenRouter
│   │   ├── __init__.py
│   │   └── openrouter_client.py  # Client OpenRouter
│   │
│   ├── models/                   # Module Models - Schémas Pydantic
│   │   ├── __init__.py
│   │   └── schemas.py            # Tous les modèles de données
│   │
│   └── tools/                    # Module Tools - Utilitaires
│       └── __init__.py
│
├── venv/                         # Environnement virtuel Python
├── .env                          # Variables d'environnement
├── .gitignore                    # Fichiers ignorés par Git
├── main.py                       # Point d'entrée à la racine (redirige vers app.main)
├── requirements.txt              # Dépendances Python
├── README.md                      # Documentation principale
└── [autres fichiers de configuration et scripts]
```

## Modules

### `app/` - Package principal
Point d'entrée de l'application FastAPI.

### `app/api/` - Routers FastAPI
- **routers.py** : Tous les endpoints de l'API organisés par domaines :
  - Routes principales (`api_router`)
  - Routes primes (`primes_router`)
  - Routes articles (`articles_router`)
  - Routes recherche (`search_router`)
  - Routes OpenRouter (`openrouter_router`)

### `app/db/` - Base de données
- **db_postgres.py** : Fonctions pour interagir avec PostgreSQL
- **db.py** : Fonctions de base de données (si nécessaire)

### `app/llm/` - Intelligence Artificielle
- **openrouter_client.py** : Client pour l'API OpenRouter avec méthodes :
  - `chat_completion()` : Chat générique
  - `analyze_prime()` : Analyse de primes
  - `generate_explanation()` : Explication d'articles
  - `search_and_explain()` : Recherche intelligente

### `app/models/` - Modèles de données
- **schemas.py** : Tous les schémas Pydantic pour la validation des données

### `app/tools/` - Utilitaires
Dossier pour les outils et utilitaires du projet.

## Imports

Tous les imports utilisent maintenant le préfixe `app.` :

```python
# Exemples d'imports
from app.api import api_router, primes_router
from app.db import code_articles, get_all_primes
from app.llm import openrouter_client
from app.models import Prime, PrimeResponse
from app.config import settings
```

## Démarrage

### Option 1 : Via le fichier main.py à la racine
```bash
python main.py
```

### Option 2 : Directement via uvicorn
```bash
uvicorn app.main:app --reload
```

## Avantages de cette structure

1. **Séparation claire des responsabilités** : Chaque module a un rôle bien défini
2. **Maintenabilité** : Code organisé et facile à naviguer
3. **Scalabilité** : Facile d'ajouter de nouveaux modules
4. **Réutilisabilité** : Modules indépendants réutilisables
5. **Testabilité** : Chaque module peut être testé indépendamment

## Migration depuis l'ancienne structure

Si vous avez des scripts qui utilisent encore les anciens imports, mettez-les à jour :

```python
# Ancien
from config import settings
from db_postgres import code_articles
from schemas import Prime
from routers import api_router

# Nouveau
from app.config import settings
from app.db import code_articles
from app.models import Prime
from app.api import api_router
```

