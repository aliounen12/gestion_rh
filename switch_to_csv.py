#!/usr/bin/env python3
"""
Script pour revenir temporairement à l'utilisation du CSV au lieu de PostgreSQL
"""

def switch_to_csv():
    print("🔄 Basculement vers l'utilisation du CSV...")
    print("=" * 50)
    
    # Modifier main.py pour utiliser db.py au lieu de db_postgres.py
    try:
        with open('main.py', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remplacer les imports
        content = content.replace(
            'from db_postgres import code_articles, get_articles_count',
            'from db import code_articles'
        )
        content = content.replace(
            'from config import settings',
            '# from config import settings'
        )
        content = content.replace(
            'print(f"🗄️  Base de données: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")',
            '# print(f"🗄️  Base de données: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")'
        )
        content = content.replace(
            'print(f"📚 Articles chargés depuis PostgreSQL: {len(code_articles)}")',
            'print(f"📚 Articles chargés depuis CSV: {len(code_articles)}")'
        )
        content = content.replace(
            'host=settings.API_HOST,',
            'host="0.0.0.0",'
        )
        content = content.replace(
            'port=settings.API_PORT,',
            'port=8000,'
        )
        content = content.replace(
            'reload=settings.DEBUG,',
            'reload=True,'
        )
        
        with open('main.py', 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("✅ main.py modifié pour utiliser le CSV")
        
        # Modifier routers.py pour utiliser db.py au lieu de db_postgres.py
        with open('routers.py', 'r', encoding='utf-8') as file:
            content = file.read()
        
        content = content.replace(
            'from db_postgres import (',
            'from db import ('
        )
        content = content.replace(
            'get_articles_count',
            ''
        )
        content = content.replace(
            'get_articles_count,',
            ''
        )
        content = content.replace(
            ', get_articles_count',
            ''
        )
        content = content.replace(
            '"API avec base de données PostgreSQL pour la gestion des primes avec conformité légale",',
            '"API simplifiée pour la gestion des primes avec conformité légale",'
        )
        content = content.replace(
            '"API fonctionnelle avec PostgreSQL",',
            '"API fonctionnelle",'
        )
        content = content.replace(
            '"Articles chargés depuis PostgreSQL - table public.articles",',
            '"Articles chargés depuis articles_structures.csv",'
        )
        content = content.replace(
            'version="4.0.0",',
            'version="3.0.0",'
        )
        
        with open('routers.py', 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("✅ routers.py modifié pour utiliser le CSV")
        
        print("\n🎉 Basculement terminé!")
        print("📚 L'API utilise maintenant le fichier articles_structures.csv")
        print("🌐 Vous pouvez démarrer l'API avec: python main.py")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    switch_to_csv()
