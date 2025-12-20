# API de Gestion des Primes - Architecture Modulaire

## Description

Cette API de gestion des primes est conforme au Code du travail Sénégalais et utilise une architecture modulaire pour une meilleure organisation et maintenabilité du code.

## Architecture

Le projet est maintenant organisé en plusieurs modules :

### 📁 Structure des fichiers

```
GestionRH/
├── main.py                    # Point d'entrée principal de l'API
├── schemas.py                 # Modèles Pydantic pour la validation des données
├── routers.py                 # Définition de tous les endpoints FastAPI
├── db.py                      # Gestion de la base de données et logique métier
├── articles_structures.csv    # Articles du Code du travail Sénégalais
└── README.md                  # Documentation du projet
```

### 🔧 Modules

#### `main.py`
- Point d'entrée de l'application FastAPI
- Configuration de l'application
- Inclusion des routers
- Démarrage automatique du serveur

#### `schemas.py`
- Définition de tous les modèles Pydantic
- Validation des données d'entrée et de sortie
- Schémas pour les réponses API

#### `routers.py`
- Définition de tous les endpoints FastAPI
- Organisation par groupes (primes, articles, recherche)
- Logique de contrôle des requêtes

#### `db.py`
- Gestion de la base de données en mémoire
- Fonctions de manipulation des données
- Logique métier pour la conformité légale

## Endpoints disponibles

### 🏠 Endpoints principaux
- `GET /` : Informations sur l'API
- `GET /test` : Test de fonctionnement

### 💰 Gestion des primes
- `POST /primes/` : Créer une nouvelle prime
- `GET /primes/` : Récupérer toutes les primes
- `GET /primes/{prime_id}` : Récupérer une prime par ID
- `GET /primes/par-type/{type_prime}` : Récupérer les primes par type
- `POST /primes/exemple` : Créer une prime d'exemple

### 📋 Types de primes
- `GET /types-primes/` : Liste des types de primes disponibles

### ⚖️ Conformité légale
- `GET /conformite/primes` : Documentation de conformité

### 📚 Articles du Code du travail
- `GET /articles/{article_code}` : Consulter un article spécifique
- `GET /search/articles` : Rechercher des articles par mot-clé

### 🤖 OpenRouter (IA)
- `POST /openrouter/chat` : Chat générique avec OpenRouter
- `POST /openrouter/analyze-prime` : Analyser une prime avec l'IA
- `POST /openrouter/explain-article` : Expliquer un article avec l'IA
- `POST /openrouter/search-explain` : Rechercher et expliquer avec l'IA
- `POST /openrouter/enhanced-prime` : Créer une prime enrichie par l'IA
- `GET /openrouter/models` : Liste des modèles disponibles

## Utilisation

### 🔧 Configuration de l'environnement virtuel

Le projet utilise un environnement virtuel Python pour isoler les dépendances.

#### Activation de l'environnement virtuel

**Windows PowerShell :**
```powershell
.\activate.ps1
```

**Windows CMD :**
```cmd
activate.bat
```

**Ou manuellement :**
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

#### Installation des dépendances

Si les dépendances ne sont pas encore installées :
```bash
pip install -r requirements.txt
```

### Démarrage du serveur

Une fois l'environnement virtuel activé :
```bash
python main.py
```

ou
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Documentation interactive
Accédez à la documentation Swagger à l'adresse :
http://localhost:8000/docs

### Exemple de création de prime
```json
{
  "type_prime": "Prime de rendement",
  "motif": "Excellente performance trimestrielle"
}
```

## Avantages de l'architecture modulaire

1. **Séparation des responsabilités** : Chaque module a un rôle bien défini
2. **Maintenabilité** : Code plus facile à maintenir et à déboguer
3. **Réutilisabilité** : Les modules peuvent être réutilisés dans d'autres projets
4. **Testabilité** : Chaque module peut être testé indépendamment
5. **Scalabilité** : Facile d'ajouter de nouvelles fonctionnalités

## Fonctionnalités

- ✅ Chargement dynamique des articles depuis PostgreSQL
- ✅ Validation des données avec Pydantic
- ✅ Recherche intelligente d'articles pertinents
- ✅ Génération automatique d'explications de conformité
- ✅ **Intégration OpenRouter pour l'analyse IA** 🤖
- ✅ Architecture modulaire et extensible
- ✅ Documentation automatique avec Swagger
- ✅ Gestion d'erreurs robuste

## 🤖 Intégration OpenRouter

L'API intègre maintenant OpenRouter pour enrichir les fonctionnalités avec l'intelligence artificielle :

- **Analyse intelligente de primes** : Analyse automatique de conformité avec l'IA
- **Explication d'articles** : Explications simplifiées des articles du Code du travail
- **Recherche contextuelle** : Recherche intelligente avec synthèse IA
- **Création enrichie** : Création de primes avec explications générées par l'IA

📖 **Voir [OPENROUTER_SETUP.md](OPENROUTER_SETUP.md) pour la configuration détaillée**

### Configuration rapide OpenRouter

1. Créez un compte sur [OpenRouter.ai](https://openrouter.ai/)
2. Obtenez votre clé API
3. Ajoutez dans votre fichier `.env` :
   ```env
   OPENROUTER_API_KEY=votre_cle_api_ici
   ```

## Version

**Version 4.1.0** - Architecture modulaire + Intégration OpenRouter
