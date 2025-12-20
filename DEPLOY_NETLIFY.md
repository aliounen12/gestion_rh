# 🚀 Déploiement sur Netlify

Guide pour déployer l'API FastAPI sur Netlify.

## 📋 Prérequis

1. Un compte Netlify (gratuit sur [netlify.com](https://www.netlify.com))
2. Git installé et configuré
3. Le projet versionné avec Git

## 🔧 Configuration

### 1. Fichiers de configuration créés

- `netlify.toml` : Configuration Netlify
- `netlify/functions/api.py` : Handler Netlify Function
- `.netlifyignore` : Fichiers à exclure du déploiement
- `requirements.txt` : Mis à jour avec `mangum`

### 2. Structure Netlify

```
gestion_rh/
├── netlify/
│   └── functions/
│       └── api.py          # Handler Netlify Function
├── netlify.toml            # Configuration Netlify
├── .netlifyignore         # Fichiers à ignorer
└── app/                   # Votre application
```

## 🚀 Déploiement

### Option 1 : Via Netlify CLI (recommandé)

1. **Installer Netlify CLI** :
   ```bash
   npm install -g netlify-cli
   ```

2. **Se connecter à Netlify** :
   ```bash
   netlify login
   ```

3. **Initialiser le site** :
   ```bash
   netlify init
   ```
   - Choisir "Create & configure a new site"
   - Suivre les instructions

4. **Déployer** :
   ```bash
   netlify deploy --prod
   ```

### Option 2 : Via Git (recommandé pour CI/CD)

1. **Pousser votre code sur GitHub/GitLab/Bitbucket**

2. **Sur Netlify Dashboard** :
   - Aller sur [app.netlify.com](https://app.netlify.com)
   - Cliquer sur "Add new site" > "Import an existing project"
   - Connecter votre dépôt Git
   - Configurer :
     - **Build command** : (laisser vide ou `echo 'No build'`)
     - **Publish directory** : `.` (racine)
     - **Functions directory** : `netlify/functions`

3. **Configurer les variables d'environnement** :
   - Aller dans "Site settings" > "Environment variables"
   - Ajouter toutes les variables de `.env` :
     ```
     DB_HOST=...
     DB_PORT=...
     DB_NAME=...
     DB_USER=...
     DB_PASSWORD=...
     OPENROUTER_API_KEY=...
     OPENROUTER_MODEL=...
     etc.
     ```

## ⚙️ Variables d'environnement

Dans Netlify Dashboard, ajoutez ces variables :

### Base de données PostgreSQL
```
DB_HOST=votre-host
DB_PORT=5432
DB_NAME=votre-db
DB_USER=votre-user
DB_PASSWORD=votre-password
```

### OpenRouter
```
OPENROUTER_API_KEY=votre-cle-api
OPENROUTER_MODEL=openai/gpt-3.5-turbo
OPENROUTER_MAX_TOKENS=1000
OPENROUTER_TEMPERATURE=0.7
```

### API
```
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
```

## 🔍 Vérification

Une fois déployé, vos endpoints seront disponibles à :
- `https://votre-site.netlify.app/.netlify/functions/api/assistant/chat`
- `https://votre-site.netlify.app/.netlify/functions/api/assistant/tools`
- `https://votre-site.netlify.app/.netlify/functions/api/gestionrh`

Grâce aux redirects dans `netlify.toml`, vous pouvez aussi accéder via :
- `https://votre-site.netlify.app/assistant/chat`
- `https://votre-site.netlify.app/assistant/tools`
- `https://votre-site.netlify.app/gestionrh`

## 📝 Notes importantes

### Limitations Netlify Functions

1. **Timeout** : 10 secondes (gratuit) ou 26 secondes (pro)
2. **Taille de payload** : 6 MB maximum
3. **Cold start** : Premier appel peut être lent
4. **PostgreSQL** : Assurez-vous que votre base de données est accessible depuis Internet

### Optimisations

1. **Connection pooling** : Utilisez un pool de connexions pour PostgreSQL
2. **Cache** : Mettez en cache les articles chargés
3. **Timeout** : Configurez des timeouts appropriés pour les appels OpenRouter

### Alternative : Base de données

Si votre PostgreSQL n'est pas accessible depuis Internet, considérez :
- **Supabase** : PostgreSQL hébergé avec accès Internet
- **Neon** : PostgreSQL serverless
- **Railway** : PostgreSQL avec accès Internet

## 🐛 Dépannage

### Erreur : "Module not found"
- Vérifiez que tous les modules sont dans `requirements.txt`
- Netlify installe automatiquement depuis `requirements.txt`

### Erreur : "Timeout"
- Les fonctions Netlify ont un timeout limité
- Optimisez vos requêtes (cache, connexions pool)

### Erreur : "Database connection failed"
- Vérifiez que votre PostgreSQL est accessible depuis Internet
- Vérifiez les variables d'environnement dans Netlify Dashboard
- Vérifiez les règles de firewall

### Logs
- Consultez les logs dans Netlify Dashboard > "Functions" > "Logs"

## 🔄 Mise à jour

Pour mettre à jour le déploiement :
```bash
git add .
git commit -m "Update"
git push
```
Netlify redéploiera automatiquement si vous avez configuré le déploiement automatique.

## 📚 Ressources

- [Netlify Functions Docs](https://docs.netlify.com/functions/overview/)
- [Mangum Documentation](https://mangum.io/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
