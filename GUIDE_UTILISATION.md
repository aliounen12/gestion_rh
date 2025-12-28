# 📖 Guide d'utilisation - ChatRH API

## 🚀 Démarrage de l'API

### 1. Activer l'environnement virtuel

**Windows PowerShell :**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD :**
```cmd
venv\Scripts\activate.bat
```

### 2. Démarrer le serveur

```bash
python main.py
```

L'API sera disponible sur : **http://localhost:8000**

## 📡 Comment utiliser l'API

### 1. Documentation interactive

Accédez à la documentation Swagger :
- **URL** : http://localhost:8000/docs
- Interface graphique pour tester tous les endpoints

### 2. Endpoint Chat - Poser des questions

**URL** : `POST http://localhost:8000/chat`

**Exemple avec cURL :**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Quels sont les droits des travailleurs concernant les congés ?",
    "model": "openai/gpt-3.5-turbo",
    "temperature": 0.7
  }'
```

**Exemple avec Python :**
```python
import requests

url = "http://localhost:8000/chat"
data = {
    "message": "Quels sont les droits des travailleurs concernant les congés ?",
    "model": "openai/gpt-3.5-turbo",
    "temperature": 0.7
}

response = requests.post(url, json=data)
result = response.json()
print(result["response"])
```

**Exemple avec JavaScript (fetch) :**
```javascript
fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Quels sont les droits des travailleurs concernant les congés ?',
    model: 'openai/gpt-3.5-turbo',
    temperature: 0.7
  })
})
.then(response => response.json())
.then(data => console.log(data.response));
```

### 3. Endpoint Health Check

**URL** : `GET http://localhost:8000/health`

**Exemple :**
```bash
curl http://localhost:8000/health
```

**Réponse :**
```json
{
  "status": "ok",
  "message": "API ChatRH opérationnelle - 281 articles disponibles dans la base de données"
}
```

## 💬 Exemples de questions à poser

### Questions sur les congés
```json
{
  "message": "Comment calculer les jours de congés payés ?"
}
```

### Questions sur le transport
```json
{
  "message": "Quels sont les frais de transport pris en charge par l'employeur ?"
}
```

### Questions générales sur le Code du travail
```json
{
  "message": "Quelles sont les obligations de l'employeur envers les travailleurs ?"
}
```

## 🔧 Paramètres de la requête Chat

### Paramètres disponibles

- **`message`** (requis) : Votre question
- **`model`** (optionnel) : Modèle à utiliser (défaut: `openai/gpt-3.5-turbo`)
- **`temperature`** (optionnel) : Créativité de la réponse (0.0 à 1.0, défaut: 0.7)

### Exemples de modèles disponibles

- `openai/gpt-3.5-turbo` (recommandé, rapide et économique)
- `openai/gpt-4` (plus précis mais plus cher)
- `anthropic/claude-3-haiku` (rapide)
- `anthropic/claude-3-sonnet` (équilibré)

## 🎯 Fonctionnement interne

Lorsque vous posez une question :

1. **Extraction des mots-clés** : Le système identifie les sujets pertinents (ex: "congés", "transport")
2. **Recherche PostgreSQL** : Les articles du Code du travail correspondants sont récupérés
3. **Enrichissement du contexte** : Les articles trouvés sont ajoutés au contexte
4. **Appel OpenRouter** : La question + le contexte sont envoyés à l'IA
5. **Réponse enrichie** : L'IA répond en s'appuyant sur les articles du Code du travail

## 📝 Réponse de l'API

**Format de réponse :**
```json
{
  "response": "Réponse détaillée de l'assistant IA...",
  "model": "openai/gpt-3.5-turbo"
}
```

## ⚠️ Erreurs possibles

### Erreur 400 - Message invalide
```json
{
  "detail": "Le message ne peut pas être vide"
}
```

### Erreur 401 - Clé API invalide
```json
{
  "detail": "Erreur d'authentification (401): Vérifiez que votre clé API OpenRouter est valide"
}
```

### Erreur 500 - Erreur serveur
```json
{
  "detail": "Erreur lors du chat: ..."
}
```

## 🔍 Test rapide

Testez rapidement avec cette commande :

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour, pouvez-vous m\'aider ?"}'
```

## 📚 Documentation complète

Pour plus de détails, consultez :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
