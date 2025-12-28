# 🚀 Guide de déploiement sur Vercel

> **✅ Configuration déjà faite** : Ce guide suppose que votre base de données PostgreSQL et les variables d'environnement sont **déjà configurées sur Vercel**.

## 📋 Prérequis

- ✅ Compte Vercel configuré
- ✅ Base de données PostgreSQL configurée (Supabase/Neon)
- ✅ Variables d'environnement configurées dans Vercel Dashboard :
  - `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
  - `OPENROUTER_API_KEY`
  - (Optionnel) `OPENROUTER_MODEL`, `OPENROUTER_MAX_TOKENS`, `OPENROUTER_TEMPERATURE`

## 📦 Étape 1 : Préparer le projet pour Vercel

### 1. Vérifier `vercel.json`

Le fichier `vercel.json` doit être présent à la racine avec cette configuration :

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.11"
  }
}
```

### 2. Vérifier le handler Vercel

Le fichier `api/index.py` doit être présent avec ce contenu :

```python
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
```

**Important** : Vercel supporte nativement ASGI, donc **pas besoin de Mangum** !

### 3. Vérifier `requirements.txt`

Le fichier `requirements.txt` doit contenir ces dépendances :

```
fastapi==0.104.1
pydantic>=2.12.0
python-dotenv==1.0.0
requests==2.31.0
psycopg2-binary==2.9.9
```

## 🚀 Étape 2 : Déployer

### Méthode 1 : Via GitHub (Recommandé)

1. Poussez votre code sur GitHub
2. Connectez votre repo à Vercel (si pas déjà fait)
3. Vercel détectera automatiquement le projet Python
4. Le déploiement se fera automatiquement avec les variables d'environnement déjà configurées

### Méthode 2 : Via Vercel CLI

```bash
# Installer Vercel CLI
npm i -g vercel

# Se connecter
vercel login

# Déployer
vercel

# Pour la production
vercel --prod
```

## 📝 Structure finale

```
gestion_rh/
├── api/
│   └── index.py          # Handler Vercel
├── app/                   # Votre application
├── vercel.json           # Configuration Vercel
├── requirements.txt      # Dépendances
└── .vercelignore        # Fichiers à ignorer
```

## ⚠️ Notes importantes

1. **Timeout** : Vercel Functions ont un timeout de 10s (gratuit) ou 60s (pro)
2. **Cold start** : Le premier appel peut être lent
3. **Base de données** : Doit être accessible depuis Internet
4. **Variables d'environnement** : Configurez-les dans Vercel Dashboard

## 📄 Note sur la base de données

> **✅ Configuration déjà faite** : Votre base de données PostgreSQL est déjà configurée et chargée sur Vercel. L'application utilisera automatiquement les variables d'environnement configurées dans Vercel Dashboard pour se connecter à votre base existante.

L'application se connecte automatiquement via :
- `DB_HOST` : Host de votre base (Supabase/Neon)
- `DB_PORT` : Port (généralement 5432)
- `DB_NAME` : Nom de la base (généralement `postgres`)
- `DB_USER` : Utilisateur PostgreSQL
- `DB_PASSWORD` : Mot de passe PostgreSQL

Ces variables sont déjà configurées dans **Vercel Dashboard > Settings > Environment Variables**.

## 🔍 Vérification

Une fois déployé, testez :
- `https://votre-projet.vercel.app/` → Infos API
- `https://votre-projet.vercel.app/chat` → Endpoint chat
- `https://votre-projet.vercel.app/health` → Health check

## 🆘 Dépannage

### Erreur : "psycopg2-binary not available"
- Vérifiez que `psycopg2-binary==2.9.9` est dans `requirements.txt`

### Erreur : "Connection timeout"
- Vérifiez que votre base de données est accessible depuis Internet
- Vérifiez les paramètres de firewall de votre base de données

### Erreur : "Function timeout"
- Les fonctions Vercel ont un timeout de 10s (gratuit)
- Considérez optimiser les requêtes ou passer au plan Pro (60s)
