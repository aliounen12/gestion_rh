# 🔧 Dépannage Netlify - Guide complet

## 🚨 Problèmes courants et solutions

### 1. Erreur : "Function failed to start"

**Symptômes** :
- Le déploiement échoue
- Erreur dans les logs : "Function failed to start"

**Solutions** :

1. **Vérifier les imports** :
   - Ouvrez Netlify Dashboard > Functions > api > Logs
   - Cherchez les erreurs d'import
   - Vérifiez que tous les modules sont dans `requirements.txt`

2. **Vérifier la structure** :
   ```
   netlify/
   └── functions/
       └── api.py  ← Doit être ici
   ```

3. **Vérifier les variables d'environnement** :
   - Netlify Dashboard > Site settings > Environment variables
   - Toutes les variables doivent être configurées

### 2. Erreur : "Module not found"

**Solution** :
```bash
# Vérifiez que requirements.txt contient :
fastapi==0.104.1
mangum==0.17.0
pydantic==2.5.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
requests==2.31.0
```

### 3. Erreur : "Timeout"

**Symptômes** :
- La fonction prend plus de 10 secondes
- Erreur 504 Gateway Timeout

**Solutions** :
- Utilisez un plan Netlify Pro (26s timeout)
- Optimisez le chargement des articles (déjà fait avec chargement lazy)
- Réduisez les appels OpenRouter (utilisez un modèle plus rapide)

### 4. Erreur : "Database connection failed"

**Solutions** :
1. Vérifiez que PostgreSQL est accessible depuis Internet
2. Vérifiez les variables d'environnement :
   ```
   DB_HOST=votre-host-public
   DB_PORT=5432
   DB_NAME=votre-db
   DB_USER=votre-user
   DB_PASSWORD=votre-password
   ```
3. Vérifiez les règles de firewall PostgreSQL
4. Testez la connexion depuis un autre serveur

### 5. Erreur : "OPENROUTER_API_KEY not configured"

**Solution** :
- Ajoutez dans Netlify Dashboard > Environment variables :
  ```
  OPENROUTER_API_KEY=votre-cle-api
  ```

### 6. Erreur : "404 Not Found" sur les endpoints

**Symptômes** :
- Les endpoints retournent 404
- Les redirects ne fonctionnent pas

**Solutions** :
1. Vérifiez `netlify.toml` :
   ```toml
   [[redirects]]
     from = "/assistant/*"
     to = "/.netlify/functions/api"
   ```

2. Testez directement :
   ```
   https://votre-site.netlify.app/.netlify/functions/api/assistant/chat
   ```

3. Vérifiez que le handler retourne bien une réponse

## 🔍 Comment vérifier les logs

1. **Netlify Dashboard** :
   - Allez sur votre site
   - "Functions" > "api" > "Logs"
   - Regardez les erreurs récentes

2. **Via Netlify CLI** :
   ```bash
   netlify logs:functions
   ```

## 🧪 Test local avant déploiement

### Option 1 : Netlify CLI

```bash
# Installer
npm install -g netlify-cli

# Tester localement
netlify dev
```

### Option 2 : Test Python

```bash
python test_netlify_handler.py
```

## 📋 Checklist de déploiement

Avant de déployer, vérifiez :

- [ ] Tous les fichiers sont dans Git
- [ ] `requirements.txt` est à jour
- [ ] `netlify.toml` est correct
- [ ] Variables d'environnement configurées dans Netlify
- [ ] PostgreSQL accessible depuis Internet
- [ ] Clé OpenRouter configurée
- [ ] Handler testé localement

## 🔄 Redéploiement

Si le déploiement échoue :

1. **Vérifier les logs** dans Netlify Dashboard
2. **Corriger les erreurs** identifiées
3. **Commit et push** :
   ```bash
   git add .
   git commit -m "Fix: description de la correction"
   git push
   ```
4. **Redéployer** :
   - Netlify redéploie automatiquement, OU
   - Netlify Dashboard > "Deploys" > "Trigger deploy" > "Clear cache and deploy site"

## 📞 Support

Si le problème persiste :

1. Consultez les logs détaillés
2. Vérifiez la documentation Netlify Functions
3. Testez avec Netlify CLI localement
4. Vérifiez que tous les fichiers nécessaires sont dans le dépôt

## 🎯 Configuration optimale

### Variables d'environnement minimales

```
# Obligatoires
OPENROUTER_API_KEY=votre-cle

# Optionnelles (avec valeurs par défaut)
OPENROUTER_MODEL=openai/gpt-3.5-turbo
OPENROUTER_MAX_TOKENS=1000
OPENROUTER_TEMPERATURE=0.7

# PostgreSQL (si utilisé)
DB_HOST=votre-host
DB_PORT=5432
DB_NAME=votre-db
DB_USER=votre-user
DB_PASSWORD=votre-password
```

### Configuration recommandée

- **Plan** : Netlify Pro (pour 26s timeout)
- **Python** : 3.11
- **Cache** : Activé pour les builds
