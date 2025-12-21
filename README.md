# ChatRH - API de Chat pour la Gestion RH

API FastAPI pour un système de chat intelligent dédié à la gestion des ressources humaines.

## 🚀 Fonctionnalités

- **Chat IA** : Interface de chat avec assistant IA via OpenRouter
- **API REST** : Endpoints simplifiés et documentés
- **Architecture modulaire** : Structure claire et extensible

## 📁 Structure du projet

```
chatrh/
├── app/
│   ├── api/
│   │   ├── chat.py          # Router pour le chat
│   │   └── health.py         # Router pour le health check
│   ├── llm/
│   │   └── openrouter_client.py  # Client OpenRouter
│   ├── models/               # Schémas Pydantic (si nécessaire)
│   ├── db/                   # Gestion base de données (optionnel)
│   ├── tools/                # Outils utilitaires (optionnel)
│   ├── config.py             # Configuration
│   └── main.py               # Application FastAPI
├── main.py                    # Point d'entrée local
├── requirements.txt          # Dépendances Python
└── README.md                 # Documentation
```

## 🔧 Installation

### 1. Créer l'environnement virtuel

**Windows PowerShell :**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac :**
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration

Créez un fichier `.env` à la racine :

```env
# OpenRouter (requis pour le chat)
OPENROUTER_API_KEY=votre_cle_api
OPENROUTER_MODEL=openai/gpt-3.5-turbo
OPENROUTER_MAX_TOKENS=1000
OPENROUTER_TEMPERATURE=0.7

# API (optionnel)
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

## 🚀 Démarrage local

```bash
python main.py
```

L'API sera disponible sur : http://localhost:8000

Documentation interactive : http://localhost:8000/docs

## 📡 Endpoints disponibles

### Chat

- **`POST /chat`** : Chat avec l'assistant IA
  ```json
  {
    "message": "Qu'est-ce qu'une prime de rendement ?",
    "model": "openai/gpt-3.5-turbo",
    "temperature": 0.7
  }
  ```

### Health Check

- **`GET /health`** : Vérification de l'état de l'API


## 🛠️ Technologies utilisées

- **FastAPI** : Framework web moderne
- **OpenRouter** : API pour accéder à différents modèles LLM
- **Pydantic** : Validation des données
- **Uvicorn** : Serveur ASGI pour FastAPI

## 📄 Licence

MIT

## 🤝 Contribution

Les contributions sont les bienvenues !
