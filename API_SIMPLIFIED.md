# 🚀 API Simplifiée - 3 Endpoints

L'API a été simplifiée pour n'exposer que 3 endpoints essentiels.

## 📋 Endpoints disponibles

### 1. POST /assistant/chat
**Chat With Assistant**

Permet de discuter avec l'assistant IA pour obtenir des informations sur la gestion des primes et le Code du travail sénégalais.

**Requête :**
```json
{
  "message": "Explique-moi les primes de rendement",
  "model": "openai/gpt-3.5-turbo",  // optionnel
  "temperature": 0.7  // optionnel
}
```

**Réponse :**
```json
{
  "response": "Les primes de rendement sont...",
  "model": "openai/gpt-3.5-turbo"
}
```

### 2. GET /assistant/tools
**Get Available Tools**

Retourne la liste des outils disponibles pour l'assistant.

**Réponse :**
```json
{
  "tools": [
    {
      "name": "chat",
      "description": "Chat avec l'assistant IA...",
      "type": "chat"
    },
    {
      "name": "analyze_prime",
      "description": "Analyser une prime...",
      "type": "analysis"
    },
    {
      "name": "explain_article",
      "description": "Expliquer un article...",
      "type": "explanation"
    },
    {
      "name": "search_articles",
      "description": "Rechercher des articles...",
      "type": "search"
    }
  ]
}
```

### 3. GET /gestionrh
**Health Check**

Vérifie l'état de l'API de gestion RH.

**Réponse :**
```json
{
  "status": "ok",
  "message": "API Gestion RH opérationnelle - 281 articles chargés"
}
```

## 🚀 Utilisation

### Démarrer l'API
```bash
python main.py
```

### Accéder à la documentation
http://localhost:8000/docs

### Tester les endpoints

**Chat :**
```bash
curl -X POST "http://localhost:8000/assistant/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Qu'est-ce qu'une prime de rendement?"}'
```

**Tools :**
```bash
curl "http://localhost:8000/assistant/tools"
```

**Health Check :**
```bash
curl "http://localhost:8000/gestionrh"
```

## 📝 Notes

- L'API utilise OpenRouter pour les fonctionnalités IA
- Assurez-vous d'avoir configuré `OPENROUTER_API_KEY` dans votre fichier `.env`
- Le health check vérifie que les articles sont bien chargés depuis PostgreSQL

