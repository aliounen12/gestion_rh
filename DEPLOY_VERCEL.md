# 🚀 Guide de déploiement sur Vercel

## 📋 Prérequis

1. Compte Vercel (gratuit) : https://vercel.com
2. Base de données PostgreSQL hébergée (options gratuites) :
   - **Supabase** (recommandé) : https://supabase.com
   - **Neon** : https://neon.tech
   - **Railway** : https://railway.app

## 🔧 Étape 1 : Migrer la base de données PostgreSQL

### Option A : Supabase (Recommandé - Gratuit)

1. **Créer un compte** sur https://supabase.com
2. **Créer un nouveau projet**
3. **Récupérer les informations de connexion** :
   - Allez dans Settings > Database
   - Host : `db.xxxxx.supabase.co`
   - Port : `5432`
   - Database : `postgres`
   - User : `postgres`
   - Password : (généré automatiquement, visible dans Settings)

4. **Migrer vos données** :

   **Méthode 1 : Via pgAdmin ou DBeaver**
   - Connectez-vous à votre ancienne base PostgreSQL
   - Exportez les tables `public.article` et `public.sujet` (Format SQL)
   - Connectez-vous à Supabase
   - Exécutez le script SQL exporté

   **Méthode 2 : Via pg_dump (ligne de commande)**
   ```bash
   # Exporter depuis votre ancienne base
   pg_dump -h ancien_host -U ancien_user -d ancien_db -t public.article -t public.sujet > migration.sql
   
   # Importer dans Supabase
   psql -h db.xxxxx.supabase.co -U postgres -d postgres -f migration.sql
   ```

   **Méthode 3 : Via Python (script de migration)**
   - Voir la section "Script de migration" ci-dessous

### Option B : Neon

1. Créez un compte sur https://neon.tech
2. Créez un projet
3. Récupérez la connection string
4. Migrez vos données de la même manière que Supabase

## 📦 Étape 2 : Préparer le projet pour Vercel

### 1. Créer `vercel.json`

Créez un fichier `vercel.json` à la racine :

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

### 2. Créer le handler Vercel

Créez `api/index.py` :

```python
from mangum import Mangum
from app.main import app

handler = Mangum(app)
```

### 3. Mettre à jour `requirements.txt`

Assurez-vous que `mangum` est présent :

```
fastapi==0.104.1
pydantic>=2.12.0
python-dotenv==1.0.0
requests==2.31.0
mangum==0.17.0
psycopg2-binary==2.9.9
```

## 🔐 Étape 3 : Configurer les variables d'environnement

Dans Vercel Dashboard :

1. Allez dans votre projet > Settings > Environment Variables
2. Ajoutez toutes les variables de `.env` :

```
OPENROUTER_API_KEY=votre_cle
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=votre_password
```

## 🚀 Étape 4 : Déployer

### Méthode 1 : Via GitHub (Recommandé)

1. Poussez votre code sur GitHub
2. Connectez votre repo à Vercel
3. Vercel détectera automatiquement le projet Python
4. Configurez les variables d'environnement
5. Déployez !

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

## 📊 Script de migration des données

Créez un fichier `migrate_db.py` pour migrer vos données :

```python
#!/usr/bin/env python3
"""
Script pour migrer les données vers une nouvelle base PostgreSQL
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Ancienne base (source)
OLD_DB = {
    "host": "ancien_host",
    "port": 5432,
    "database": "ancien_db",
    "user": "ancien_user",
    "password": "ancien_password"
}

# Nouvelle base (destination - Supabase/Neon)
NEW_DB = {
    "host": "db.xxxxx.supabase.co",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "nouveau_password"
}

def migrate_table(conn_old, conn_new, table_name):
    """Migre une table de l'ancienne vers la nouvelle base"""
    cursor_old = conn_old.cursor(cursor_factory=RealDictCursor)
    cursor_new = conn_new.cursor()
    
    # Récupérer les données
    cursor_old.execute(f"SELECT * FROM {table_name}")
    rows = cursor_old.fetchall()
    
    print(f"Migration de {len(rows)} lignes de {table_name}...")
    
    # Insérer dans la nouvelle base
    for row in rows:
        columns = ', '.join(row.keys())
        placeholders = ', '.join(['%s'] * len(row))
        values = tuple(row.values())
        
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
        cursor_new.execute(query, values)
    
    conn_new.commit()
    cursor_old.close()
    cursor_new.close()
    print(f"✅ {table_name} migré avec succès")

# Connexions
conn_old = psycopg2.connect(**OLD_DB)
conn_new = psycopg2.connect(**NEW_DB)

try:
    # Migrer les tables
    migrate_table(conn_old, conn_new, "public.sujet")
    migrate_table(conn_old, conn_new, "public.article")
    print("\n✅ Migration terminée avec succès !")
except Exception as e:
    print(f"❌ Erreur lors de la migration: {e}")
finally:
    conn_old.close()
    conn_new.close()
```

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
