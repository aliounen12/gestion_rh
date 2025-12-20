# 📖 Guide d'utilisation - Comment poser des questions

Guide complet pour utiliser l'API et poser des questions à l'assistant IA.

## 🚀 Démarrage rapide

### 1. Démarrer l'API

```bash
# Activer l'environnement virtuel
.\activate.ps1

# Démarrer l'API
python main.py
```

L'API sera disponible sur : `http://localhost:8000`

## 💬 Poser des questions à l'assistant

### Méthode 1 : Via l'interface Swagger (le plus simple)

1. Ouvrez votre navigateur
2. Allez sur : `http://localhost:8000/docs`
3. Trouvez l'endpoint **POST /assistant/chat**
4. Cliquez sur "Try it out"
5. Entrez votre question dans le champ `message` :
   ```json
   {
     "message": "Qu'est-ce qu'une prime de rendement ?"
   }
   ```
6. Cliquez sur "Execute"
7. La réponse de l'assistant apparaîtra en bas

### Méthode 2 : Via curl (ligne de commande)

```bash
curl -X POST "http://localhost:8000/assistant/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Qu'est-ce qu'une prime de rendement ?\"}"
```

### Méthode 3 : Via Python

```python
import requests

url = "http://localhost:8000/assistant/chat"
data = {
    "message": "Qu'est-ce qu'une prime de rendement ?"
}

response = requests.post(url, json=data)
print(response.json())
```

### Méthode 4 : Via JavaScript/Fetch

```javascript
fetch('http://localhost:8000/assistant/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: "Qu'est-ce qu'une prime de rendement ?"
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 📝 Exemples de questions

### Questions sur les primes

```json
{
  "message": "Qu'est-ce qu'une prime de rendement ?"
}
```

```json
{
  "message": "Quelles sont les conditions d'attribution d'une prime d'ancienneté ?"
}
```

```json
{
  "message": "Explique-moi la différence entre une prime de risque et une prime de résultat"
}
```

### Questions sur le Code du travail

```json
{
  "message": "Quels sont les articles du Code du travail sénégalais qui concernent les primes ?"
}
```

```json
{
  "message": "Quelles sont les obligations légales pour verser une prime ?"
}
```

### Questions générales RH

```json
{
  "message": "Comment calculer une prime de fin d'année ?"
}
```

```json
{
  "message": "Quelles sont les bonnes pratiques pour la gestion des primes ?"
}
```

## ⚙️ Options avancées

### Choisir un modèle spécifique

```json
{
  "message": "Explique-moi les primes",
  "model": "openai/gpt-4"
}
```

### Ajuster la créativité (temperature)

```json
{
  "message": "Explique-moi les primes",
  "temperature": 0.9
}
```

- `temperature: 0.0` = Réponses très précises et déterministes
- `temperature: 0.7` = Équilibre (par défaut)
- `temperature: 1.0` = Réponses plus créatives

### Exemple complet avec options

```json
{
  "message": "Donne-moi un exemple de calcul de prime de rendement",
  "model": "openai/gpt-3.5-turbo",
  "temperature": 0.8
}
```

## 🔍 Autres endpoints utiles

### Vérifier l'état de l'API

```bash
curl http://localhost:8000/gestionrh
```

Réponse :
```json
{
  "status": "ok",
  "message": "API Gestion RH opérationnelle - 281 articles chargés"
}
```

### Voir les outils disponibles

```bash
curl http://localhost:8000/assistant/tools
```

Réponse :
```json
{
  "tools": [
    {
      "name": "chat",
      "description": "Chat avec l'assistant IA...",
      "type": "chat"
    },
    ...
  ]
}
```

## 📚 Documentation interactive

La meilleure façon de tester l'API est d'utiliser la documentation Swagger :

1. **Démarrer l'API** : `python main.py`
2. **Ouvrir** : `http://localhost:8000/docs`
3. **Tester** : Cliquez sur chaque endpoint et utilisez "Try it out"

## 🌐 Sur Netlify (après déploiement)

Une fois déployé sur Netlify, remplacez `http://localhost:8000` par votre URL Netlify :

```bash
curl -X POST "https://votre-site.netlify.app/assistant/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Qu'est-ce qu'une prime de rendement ?\"}"
```

## 💡 Conseils

1. **Soyez spécifique** : Plus votre question est précise, meilleure sera la réponse
2. **Utilisez le contexte** : Mentionnez "Code du travail sénégalais" si nécessaire
3. **Testez différents modèles** : GPT-4 pour des réponses plus détaillées
4. **Ajustez la température** : Pour des réponses plus créatives ou plus précises

## 🐛 Dépannage

### Erreur : "OPENROUTER_API_KEY n'est pas configurée"

**Solution** : Ajoutez votre clé API dans le fichier `.env` :
```
OPENROUTER_API_KEY=votre_cle_api_ici
```

### Erreur : "Connection refused"

**Solution** : Vérifiez que l'API est bien démarrée avec `python main.py`

### Erreur : "Timeout"

**Solution** : 
- Vérifiez votre connexion internet
- Vérifiez que votre clé OpenRouter est valide
- Réessayez avec un modèle plus rapide (gpt-3.5-turbo)

## 📞 Exemples de réponses

### Question simple
**Question** : "Qu'est-ce qu'une prime ?"

**Réponse attendue** : L'assistant expliquera ce qu'est une prime selon le Code du travail sénégalais.

### Question complexe
**Question** : "Comment calculer une prime de rendement basée sur les performances trimestrielles ?"

**Réponse attendue** : L'assistant fournira une explication détaillée avec les articles pertinents du Code du travail.
