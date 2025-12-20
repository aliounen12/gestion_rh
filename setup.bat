@echo off
REM Script de configuration de l'environnement virtuel pour Windows
REM Usage: setup.bat

echo 🚀 Configuration de l'environnement virtuel...

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou n'est pas dans le PATH
    pause
    exit /b 1
)

REM Créer l'environnement virtuel s'il n'existe pas
if not exist "venv" (
    echo 📦 Création de l'environnement virtuel...
    python -m venv venv
    echo ✅ Environnement virtuel créé
) else (
    echo ✅ Environnement virtuel existe déjà
)

REM Activer l'environnement virtuel
echo 🔄 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Mettre à jour pip
echo 📦 Mise à jour de pip...
python -m pip install --upgrade pip

REM Installer les dépendances
echo 📦 Installation des dépendances...
pip install -r requirements.txt

echo.
echo ✅ Configuration terminée !
echo.
echo Pour activer l'environnement virtuel, utilisez:
echo   venv\Scripts\activate.bat
echo.
echo Pour démarrer l'API:
echo   python main.py
echo.
pause
