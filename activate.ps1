# Script PowerShell pour activer l'environnement virtuel
Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1
Write-Host "Environnement virtuel activé !" -ForegroundColor Green
Write-Host "Pour démarrer l'API, exécutez: python main.py" -ForegroundColor Yellow
