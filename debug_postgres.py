#!/usr/bin/env python3
"""
Script de diagnostic pour identifier le problème avec la table PostgreSQL
"""

def debug_postgres_table():
    print("🔍 Diagnostic de la table PostgreSQL...")
    print("=" * 50)
    
    try:
        # Import de la configuration
        from app.config import settings
        print(f"✅ Configuration chargée")
        print(f"   Host: {settings.DB_HOST}")
        print(f"   Database: {settings.DB_NAME}")
        print(f"   User: {settings.DB_USER}")
        
        # Test de connexion
        import psycopg2
        import psycopg2.extras
        
        connection = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        print("✅ Connexion PostgreSQL réussie")
        
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # 1. Vérifier l'existence de la table
        print("\n📊 Vérification de la table...")
        cursor.execute("""
            SELECT table_name, table_schema 
            FROM information_schema.tables 
            WHERE table_name = 'articles' AND table_schema = 'public'
        """)
        
        table_exists = cursor.fetchone()
        if table_exists:
            print(f"✅ Table trouvée: {table_exists['table_schema']}.{table_exists['table_name']}")
        else:
            print("❌ Table 'public.articles' non trouvée")
            return
        
        # 2. Vérifier les colonnes
        print("\n📋 Vérification des colonnes...")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'articles' AND table_schema = 'public'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        print(f"✅ Colonnes trouvées ({len(columns)}):")
        for col in columns:
            print(f"   - {col['column_name']} ({col['data_type']})")
        
        # 3. Compter les enregistrements
        print("\n📈 Nombre d'enregistrements...")
        cursor.execute("SELECT COUNT(*) FROM public.articles")
        count = cursor.fetchone()[0]
        print(f"✅ Nombre d'articles: {count}")
        
        # 4. Afficher quelques exemples
        print("\n📖 Exemples d'articles (5 premiers)...")
        cursor.execute("SELECT * FROM public.articles LIMIT 5")
        samples = cursor.fetchall()
        
        for i, row in enumerate(samples, 1):
            print(f"\n   Article {i}:")
            for col_name, value in row.items():
                # Limiter l'affichage du contenu
                if isinstance(value, str) and len(value) > 100:
                    display_value = value[:100] + "..."
                else:
                    display_value = value
                print(f"     {col_name}: {display_value}")
        
        # 5. Vérifier s'il y a des données
        if count == 0:
            print("\n⚠️  ATTENTION: La table est vide!")
            print("💡 Vous devez charger les données du CSV dans PostgreSQL")
        
        cursor.close()
        connection.close()
        
        print("\n✅ Diagnostic terminé")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_postgres_table()
