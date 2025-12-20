# 🔧 Corrections pour le déploiement Netlify

## Problèmes corrigés

### 1. Handler Netlify Function amélioré
- Gestion d'erreurs améliorée
- Meilleure gestion des imports
- Messages d'erreur plus clairs

### 2. Redirects optimisés
- Redirects spécifiques au lieu d'un redirect global
- Meilleure compatibilité avec Netlify

## 🚀 Déploiement

### Étapes

1. **Vérifier les fichiers** :
   ```bash
   git status
   ```

2. **Ajouter les modifications** :
   ```bash
   git add .
   git commit -m "Fix Netlify deployment"
   git push
   ```

3. **Sur Netlify Dashboard** :
   - Aller dans votre site
   - "Deploys" > "Trigger deploy" > "Clear cache and deploy site"

## 🔍 Vérification des erreurs

### Consulter les logs Netlify

1. Aller sur Netlify Dashboard
2. Sélectionner votre site
3. "Functions" > "api" > "Logs"
4. Vérifier les erreurs

### Erreurs courantes et solutions

#### "Module not found"
**Solution** : Vérifiez que `requirements.txt` contient toutes les dépendances

#### "Handler not initialized"
**Solution** : 
- Vérifiez les logs pour voir l'erreur d'import exacte
- Vérifiez que tous les fichiers sont bien dans le dépôt Git
- Vérifiez que `.netlifyignore` n'exclut pas des fichiers nécessaires

#### "Timeout"
**Solution** :
- Les fonctions Netlify ont un timeout de 10s (gratuit)
- Optimisez le chargement des articles (cache)
- Utilisez un plan Pro pour 26s de timeout

#### "Database connection failed"
**Solution** :
- Vérifiez que PostgreSQL est accessible depuis Internet
- Vérifiez les variables d'environnement dans Netlify
- Vérifiez les règles de firewall

## 📝 Variables d'environnement requises

Assurez-vous d'avoir configuré dans Netlify Dashboard :

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

## 🧪 Test local avec Netlify CLI

Pour tester localement avant de déployer :

```bash
# Installer Netlify CLI
npm install -g netlify-cli

# Tester localement
netlify dev
```

Cela démarrera un serveur local qui simule l'environnement Netlify.

## 📚 Structure des fichiers

Assurez-vous que cette structure est respectée :

```
gestion_rh/
├── netlify/
│   └── functions/
│       └── api.py          # Handler Netlify Function
├── netlify.toml            # Configuration
├── requirements.txt        # Dépendances
└── app/                   # Application
```

## ⚠️ Notes importantes

1. **Premier déploiement** : Peut prendre 5-10 minutes
2. **Cold start** : Le premier appel après inactivité peut être lent
3. **Logs** : Consultez toujours les logs en cas d'erreur
4. **Cache** : Netlify met en cache les builds, utilisez "Clear cache and deploy" si nécessaire
