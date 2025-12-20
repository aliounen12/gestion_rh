#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion à la table PostgreSQL public.articles
"""

def test_connection():
    print("🔍 Test de connexion à la table PostgreSQL public.articles...")
    print("=" * 60)
    
    try:
        # Test de la configuration
        print("📋 Test de la configuration...")
        from app.config import settings
        print(f"✅ Configuration chargée")
        print(f"   Host: {settings.DB_HOST}")
        print(f"   Port: {settings.DB_PORT}")
        print(f"   Database: {settings.DB_NAME}")
        print(f"   User: {settings.DB_USER}")
        print(f"   URL: {settings.DATABASE_URL}")
        
        # Test de la connexion et des données
        print("\n🔗 Test de la connexion...")
        from app.db import get_db_connection, load_articles_from_postgres, get_articles_count
        
        # Test avec connexion directe
        connection = get_db_connection()
        if not connection:
            print("❌ Impossible de se connecter à PostgreSQL")
            return False
        
        print("✅ Connexion à PostgreSQL réussie!")
        
        # Test de la table
        print("\n📊 Test de la table public.articles...")
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM public.articles")
        count = cursor.fetchone()[0]
        print(f"✅ Table trouvée avec {count} articles")
        
        # Test des colonnes
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'articles' AND table_schema = 'public'")
        columns = [row[0] for row in cursor.fetchall()]
        print(f"✅ Colonnes trouvées: {', '.join(columns)}")
        
        # Test de chargement des articles
        print("\n📚 Test de chargement des articles...")
        articles = load_articles_from_postgres()
        print(f"✅ {len(articles)} articles chargés depuis PostgreSQL")
        
        # Afficher quelques exemples
        if articles:
            print("\n📖 Exemples d'articles chargés:")
            for i, (code, content) in enumerate(list(articles.items())[:3]):
                print(f"   {i+1}. {code}: {content[:100]}...")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 Tous les tests ont réussi!")
        print("✅ L'API peut maintenant utiliser la table PostgreSQL public.articles")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("\n🔧 Vérifiez que:")
        print("   1. PostgreSQL est installé et démarré")
        print("   2. La base de données 'gestion_rh_db' existe")
        print("   3. La table 'public.articles' existe avec les colonnes 'article_code' et 'contenu'")
        print("   4. Les paramètres de connexion dans config.py sont corrects")
        print("   5. L'utilisateur PostgreSQL a les droits nécessaires")
        return False

if __name__ == "__main__":
    test_connection()
