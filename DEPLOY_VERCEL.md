# 🚀 Guide de déploiement sur Vercel

L’application **n’utilise pas de base SQL** : le Code du travail est lu depuis un **fichier `.docx`** présent dans le dépôt (ou dont le chemin est donné par `CODE_TRAVAIL_PATH`).

## 📋 Prérequis

- Compte Vercel configuré
- Variables d’environnement sur Vercel :
  - **`OPENROUTER_API_KEY`** (obligatoire pour `/chat`)
  - (Optionnel) `OPENROUTER_MODEL`, `OPENROUTER_MAX_TOKENS`, `OPENROUTER_TEMPERATURE`
  - (Optionnel) **`CODE_TRAVAIL_PATH`** : chemin relatif au projet vers le `.docx` (ex. `Code_sn.docx`). Si vide, l’app essaie les noms par défaut à la racine.

## 📦 Étape 1 : Préparer le projet pour Vercel

### 1. Vérifier `vercel.json`

```json
{
  "version": 2,
  "builds": [
    { "src": "api/index.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "api/index.py" }
  ]
}
```

> **Pourquoi `builds` ?** Sans cette section, des `routes` / `rewrites` seules vers `api/index.py` donnent souvent une **404**. Ne pas ajouter `functions.api/**/*.py` : le build peut échouer ([motif sans correspondance](https://vercel.link/unmatched-function-pattern)). Utiliser `.vercelignore` pour limiter le bundle.

### 2. Handler `api/index.py`

Le fichier doit importer l’app FastAPI depuis `app.main` et exposer `app` (ASGI).

### 3. `requirements.txt`

Sans `psycopg2` : par ex. `fastapi`, `pydantic`, `python-dotenv`, `requests`, etc. (voir le fichier à la racine du repo).

### 4. Fichier Word

Le `.docx` du Code du travail doit être **versionné** (ou fourni autrement) pour être inclus dans le déploiement. Vercel ne monte pas de disque persistant : pas de DOCX uniquement sur ta machine.

## 🚀 Étape 2 : Déployer

### Via GitHub

1. Push du code sur GitHub  
2. Projet lié à Vercel  
3. Définir les variables d’environnement dans **Settings → Environment Variables**  
4. Déploiement automatique

### Via CLI

```bash
npm i -g vercel
vercel login
vercel
vercel --prod
```

## 📝 Structure utile

```
gestion_rh/
├── api/index.py
├── app/
├── vercel.json
├── requirements.txt
├── .vercelignore
└── Code_sn.docx   (ou autre, selon CODE_TRAVAIL_PATH)
```

## ⚠️ Notes

1. **Timeout** : fonctions Vercel 10 s (gratuit) ou 60 s (pro)  
2. **Cold start** possible au premier appel  
3. **Taille du bundle** : le DOCX compte dans la limite de la fonction  

## 🔍 Vérification

- Racine : `https://votre-projet.vercel.app/`  
- Santé : `https://votre-projet.vercel.app/health` (articles chargés depuis le DOCX)  
- Diagnostic : `https://votre-projet.vercel.app/diagnostic`  
- Chat : `POST https://votre-projet.vercel.app/chat`  

## 🆘 Dépannage

### Chat / OpenRouter

- Vérifier `OPENROUTER_API_KEY` dans Vercel et le diagnostic (`openrouter.api_key_configured`).  
- Vérifier `OPENROUTER_MODEL` (format `fournisseur/modele`, ex. `openai/gpt-4o-mini`).

### Aucun article / erreur DOCX

- Vérifier que le fichier est bien dans le repo déployé.  
- Définir `CODE_TRAVAIL_PATH` si le fichier n’est pas un des noms par défaut.  
- Consulter `diagnostic` → `data_source`.

### Timeout

- OpenRouter est limité à 8 s côté client pour limiter les timeouts Vercel.
