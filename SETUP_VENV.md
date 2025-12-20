# 🐍 Configuration de l'environnement virtuel

Ce guide explique comment utiliser l'environnement virtuel Python pour ce projet.

## ✅ Environnement virtuel créé

Un environnement virtuel (`venv`) a été créé dans le dossier du projet. Toutes les dépendances sont installées.

## 🚀 Utilisation

### Activation de l'environnement virtuel

#### Option 1 : Scripts automatiques (recommandé)

**Windows PowerShell :**
```powershell
.\activate.ps1
```

**Windows CMD :**
```cmd
activate.bat
```

#### Option 2 : Activation manuelle

**Windows PowerShell :**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD :**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac :**
```bash
source venv/bin/activate
```

### Vérification

Une fois activé, vous devriez voir `(venv)` au début de votre ligne de commande :
```
(venv) PS C:\Users\LENOVO\Desktop\gestion_rh>
```

### Démarrer l'API

Une fois l'environnement virtuel activé :
```bash
python main.py
```

### Désactivation

Pour désactiver l'environnement virtuel :
```bash
deactivate
```

## 📦 Dépendances installées

Les packages suivants sont installés dans le venv :

- `fastapi==0.104.1` - Framework web
- `uvicorn[standard]==0.24.0` - Serveur ASGI
- `pydantic==2.5.0` - Validation de données
- `psycopg2-binary==2.9.9` - Driver PostgreSQL
- `python-dotenv==1.0.0` - Gestion des variables d'environnement
- `requests==2.31.0` - Client HTTP pour OpenRouter

## 🔄 Réinstaller les dépendances

Si vous devez réinstaller les dépendances :

```bash
# Activer le venv d'abord
.\venv\Scripts\Activate.ps1

# Réinstaller
pip install -r requirements.txt
```

## ⚠️ Notes importantes

1. **Toujours activer le venv** avant d'exécuter le projet
2. Le dossier `venv/` est dans `.gitignore` et ne sera pas versionné
3. Si vous clonez le projet ailleurs, vous devrez recréer le venv :
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

## 🐛 Dépannage

### Erreur : "Activate.ps1 cannot be loaded"

Si PowerShell bloque l'exécution de scripts, exécutez :
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erreur : "python n'est pas reconnu"

Assurez-vous que Python est installé et dans le PATH. Vérifiez avec :
```bash
python --version
```

### Erreur lors de l'installation des dépendances

Réinstallez pip et certifi :
```bash
.\venv\Scripts\python.exe -m pip install --upgrade pip certifi
pip install -r requirements.txt
```

