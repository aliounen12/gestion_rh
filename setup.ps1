# Script de configuration de l'environnement virtuel
# Usage: .\setup.ps1

Write-Host "🚀 Configuration de l'environnement virtuel..." -ForegroundColor Green

# Vérifier si Python est installé
try {
    $pythonVersion = python --version
    Write-Host "✅ Python détecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python n'est pas installé ou n'est pas dans le PATH" -ForegroundColor Red
    exit 1
}

# Créer l'environnement virtuel s'il n'existe pas
if (-not (Test-Path "venv")) {
    Write-Host "📦 Création de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Environnement virtuel créé" -ForegroundColor Green
} else {
    Write-Host "✅ Environnement virtuel existe déjà" -ForegroundColor Green
}

# Activer l'environnement virtuel
Write-Host "🔄 Activation de l'environnement virtuel..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Mettre à jour pip
Write-Host "📦 Mise à jour de pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Installer les dépendances
Write-Host "📦 Installation des dépendances..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "✅ Configuration terminée !" -ForegroundColor Green
Write-Host ""
Write-Host "Pour activer l'environnement virtuel, utilisez:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Pour démarrer l'API:" -ForegroundColor Cyan
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""
