# ⚡ Déploiement Rapide sur Netlify

## 🚀 Étapes rapides

### 1. Préparer le dépôt Git

```bash
# Initialiser Git si ce n'est pas déjà fait
git init
git add .
git commit -m "Initial commit - Ready for Netlify"
```

### 2. Pousser sur GitHub/GitLab/Bitbucket

```bash
# Créer un dépôt sur GitHub, puis :
git remote add origin https://github.com/votre-username/votre-repo.git
git push -u origin main
```

### 3. Déployer sur Netlify

#### Option A : Via Netlify Dashboard (le plus simple)

1. Aller sur [app.netlify.com](https://app.netlify.com)
2. Cliquer sur **"Add new site"** > **"Import an existing project"**
3. Connecter votre dépôt Git (GitHub/GitLab/Bitbucket)
4. Configurer :
   - **Build command** : (laisser vide)
   - **Publish directory** : `.` (point)
   - **Functions directory** : `netlify/functions`
5. Cliquer sur **"Deploy site"**

#### Option B : Via Netlify CLI

```bash
# Installer Netlify CLI
npm install -g netlify-cli

# Se connecter
netlify login

# Déployer
netlify deploy --prod
```

### 4. Configurer les variables d'environnement

Dans Netlify Dashboard :
1. Aller dans **"Site settings"** > **"Environment variables"**
2. Ajouter toutes les variables de votre `.env` :

```
DB_HOST=votre-host
DB_PORT=5432
DB_NAME=votre-db
DB_USER=votre-user
DB_PASSWORD=votre-password
OPENROUTER_API_KEY=votre-cle
OPENROUTER_MODEL=openai/gpt-3.5-turbo
OPENROUTER_MAX_TOKENS=1000
OPENROUTER_TEMPERATURE=0.7
```

### 5. Redéployer

Après avoir ajouté les variables d'environnement :
- Netlify redéploiera automatiquement, OU
- Aller dans **"Deploys"** > **"Trigger deploy"** > **"Clear cache and deploy site"**

## ✅ Vérification

Vos endpoints seront disponibles à :
- `https://votre-site.netlify.app/assistant/chat`
- `https://votre-site.netlify.app/assistant/tools`
- `https://votre-site.netlify.app/gestionrh`

## 📝 Fichiers créés pour Netlify

- ✅ `netlify.toml` - Configuration Netlify
- ✅ `netlify/functions/api.py` - Handler Netlify Function
- ✅ `.netlifyignore` - Fichiers à exclure
- ✅ `runtime.txt` - Version Python
- ✅ `package.json` - Pour Netlify
- ✅ `requirements.txt` - Mis à jour avec `mangum`

## ⚠️ Points importants

1. **PostgreSQL** : Votre base de données doit être accessible depuis Internet
2. **Timeout** : Netlify Functions a un timeout de 10s (gratuit) ou 26s (pro)
3. **Cold start** : Le premier appel peut être lent
4. **Variables d'environnement** : N'oubliez pas de les configurer dans Netlify Dashboard

## 🐛 Problèmes courants

### "Module not found"
- Vérifiez que `mangum` est dans `requirements.txt`
- Netlify installe automatiquement depuis `requirements.txt`

### "Database connection failed"
- Vérifiez que PostgreSQL est accessible depuis Internet
- Vérifiez les variables d'environnement dans Netlify

### "Timeout"
- Optimisez vos requêtes
- Utilisez un plan Netlify Pro pour 26s de timeout

## 📚 Documentation complète

Voir `DEPLOY_NETLIFY.md` pour plus de détails.
