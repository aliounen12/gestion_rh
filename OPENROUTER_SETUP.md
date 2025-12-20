# 🤖 Configuration OpenRouter

Ce guide explique comment configurer et utiliser l'intégration OpenRouter dans l'API de gestion des primes.

## 📋 Prérequis

1. Un compte sur [OpenRouter.ai](https://openrouter.ai/)
2. Une clé API OpenRouter (gratuite ou payante selon votre usage)

## 🔑 Configuration

### 1. Obtenir une clé API OpenRouter

1. Créez un compte sur [https://openrouter.ai/](https://openrouter.ai/)
2. Allez dans votre dashboard et créez une clé API
3. Copiez votre clé API

### 2. Configurer la clé API

Créez un fichier `.env` à la racine du projet (ou modifiez celui existant) :

```env
# OpenRouter Configuration
OPENROUTER_API_KEY=votre_cle_api_ici
OPENROUTER_MODEL=openai/gpt-3.5-turbo
OPENROUTER_MAX_TOKENS=1000
OPENROUTER_TEMPERATURE=0.7
```

### 3. Modèles disponibles

OpenRouter supporte de nombreux modèles. Voici quelques exemples :

- `openai/gpt-3.5-turbo` (recommandé pour débuter, économique)
- `openai/gpt-4` (plus puissant, plus cher)
- `openai/gpt-4-turbo` (version améliorée de GPT-4)
- `anthropic/claude-3-opus` (excellent pour l'analyse)
- `anthropic/claude-3-sonnet` (bon équilibre qualité/prix)
- `anthropic/claude-3-haiku` (rapide et économique)
- `google/gemini-pro` (alternative Google)
- `mistralai/mistral-medium` (open source)

## 🚀 Utilisation

### Endpoints disponibles

#### 1. Chat générique
```http
POST /openrouter/chat
Content-Type: application/json

{
  "prompt": "Explique-moi les primes de rendement",
  "system_prompt": "Tu es un expert en droit du travail",
  "model": "openai/gpt-3.5-turbo",
  "temperature": 0.7,
  "max_tokens": 500
}
```

#### 2. Analyser une prime
```http
POST /openrouter/analyze-prime
Content-Type: application/json

{
  "type_prime": "Prime de rendement",
  "motif": "Excellente performance trimestrielle",
  "articles_context": ["Art.L.30", "Art.L.31"]
}
```

#### 3. Expliquer un article
```http
POST /openrouter/explain-article
Content-Type: application/json

{
  "article_code": "Art.L.30",
  "question": "Comment cet article s'applique-t-il aux primes ?"
}
```

#### 4. Rechercher et expliquer
```http
POST /openrouter/search-explain
Content-Type: application/json

{
  "keyword": "rémunération"
}
```

#### 5. Créer une prime enrichie par l'IA
```http
POST /openrouter/enhanced-prime
Content-Type: application/json

{
  "type_prime": "Prime de rendement",
  "motif": "Performance exceptionnelle"
}
```

#### 6. Liste des modèles
```http
GET /openrouter/models
```

## 💡 Exemples d'utilisation

### Exemple 1 : Analyser une prime avec l'IA

```python
import requests

url = "http://localhost:8000/openrouter/analyze-prime"
data = {
    "type_prime": "Prime de rendement",
    "motif": "Excellente performance trimestrielle Q1 2024"
}

response = requests.post(url, json=data)
print(response.json()["analyse"])
```

### Exemple 2 : Expliquer un article

```python
import requests

url = "http://localhost:8000/openrouter/explain-article"
data = {
    "article_code": "Art.L.30",
    "question": "Quelles sont les conditions d'attribution des primes selon cet article ?"
}

response = requests.post(url, json=data)
print(response.json()["explication"])
```

### Exemple 3 : Recherche intelligente

```python
import requests

url = "http://localhost:8000/openrouter/search-explain"
data = {
    "keyword": "rémunération"
}

response = requests.post(url, json=data)
print(f"Articles trouvés: {response.json()['nombre_articles']}")
print(f"Explication: {response.json()['explication']}")
```

## 🔧 Configuration avancée

### Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `OPENROUTER_API_KEY` | Votre clé API OpenRouter | (requis) |
| `OPENROUTER_API_URL` | URL de l'API OpenRouter | `https://openrouter.ai/api/v1/chat/completions` |
| `OPENROUTER_MODEL` | Modèle par défaut | `openai/gpt-3.5-turbo` |
| `OPENROUTER_MAX_TOKENS` | Nombre max de tokens | `1000` |
| `OPENROUTER_TEMPERATURE` | Température (0-1) | `0.7` |

### Personnalisation

Vous pouvez modifier le comportement par défaut dans `config.py` ou via les variables d'environnement.

## ⚠️ Notes importantes

1. **Coûts** : L'utilisation d'OpenRouter peut engendrer des coûts selon le modèle choisi. Consultez [les tarifs](https://openrouter.ai/models) avant d'utiliser des modèles premium.

2. **Limites de taux** : OpenRouter peut avoir des limites de taux selon votre plan. Gérez vos appels en conséquence.

3. **Gestion d'erreurs** : L'API gère automatiquement les erreurs. Si OpenRouter n'est pas disponible, les fonctionnalités de base continuent de fonctionner.

4. **Sécurité** : Ne commitez jamais votre clé API dans le dépôt Git. Utilisez toujours un fichier `.env` qui est dans `.gitignore`.

## 🐛 Dépannage

### Erreur : "OPENROUTER_API_KEY n'est pas configurée"

**Solution** : Vérifiez que :
- Le fichier `.env` existe à la racine du projet
- La variable `OPENROUTER_API_KEY` est définie
- Le fichier `.env` est chargé (vérifiez que `python-dotenv` est installé)

### Erreur : "Erreur lors de l'appel à OpenRouter"

**Solutions possibles** :
- Vérifiez votre connexion internet
- Vérifiez que votre clé API est valide
- Vérifiez que vous avez des crédits disponibles sur OpenRouter
- Vérifiez les limites de taux de votre compte

### L'IA ne répond pas comme attendu

**Solutions** :
- Ajustez le `temperature` (plus bas = plus déterministe, plus haut = plus créatif)
- Modifiez le `system_prompt` pour mieux guider l'IA
- Essayez un modèle différent (GPT-4 au lieu de GPT-3.5 par exemple)

## 📚 Documentation

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [OpenRouter Models](https://openrouter.ai/models)
- [OpenRouter Pricing](https://openrouter.ai/docs/pricing)

## ✅ Test de l'intégration

Pour tester que tout fonctionne :

```bash
# 1. Vérifier que la clé API est configurée
python -c "from config import settings; print('✅ Clé API configurée' if settings.OPENROUTER_API_KEY else '❌ Clé API manquante')"

# 2. Démarrer l'API
python main.py

# 3. Tester un endpoint
curl -X POST http://localhost:8000/openrouter/models
```

## 🎯 Cas d'usage

1. **Analyse automatique de conformité** : Utilisez `/openrouter/analyze-prime` pour analyser automatiquement la conformité des primes
2. **Explication d'articles** : Utilisez `/openrouter/explain-article` pour expliquer des articles complexes
3. **Recherche intelligente** : Utilisez `/openrouter/search-explain` pour des recherches contextuelles
4. **Création enrichie** : Utilisez `/openrouter/enhanced-prime` pour créer des primes avec des explications IA
