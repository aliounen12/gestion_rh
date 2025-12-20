#!/usr/bin/env python3
"""
Script pour charger les données du CSV vers la table PostgreSQL public.articles
"""

import csv
import psycopg2
import psycopg2.extras
from app.config import settings

def load_csv_to_postgres():
    print("📊 Chargement du CSV vers PostgreSQL...")
    print("=" * 50)
    
    try:
        # Connexion à PostgreSQL
        connection = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        print("✅ Connexion à PostgreSQL réussie")
        
        cursor = connection.cursor()
        
        # 1. Vérifier si la table existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = 'articles'
            );
        """)
        
        table_exists = cursor.fetchone()[0]
        if not table_exists:
            print("❌ Table 'public.articles' n'existe pas")
            print("💡 Créez d'abord la table avec les colonnes 'article_code' et 'contenu'")
            return
        
        print("✅ Table 'public.articles' trouvée")
        
        # 2. Vider la table (optionnel)
        print("🗑️  Suppression des données existantes...")
        cursor.execute("DELETE FROM public.articles")
        connection.commit()
        print("✅ Table vidée")
        
        # 3. Charger les données du CSV
        print("📚 Chargement des données depuis articles_structures.csv...")
        
        loaded_count = 0
        with open('articles_structures.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                article_code = row['Article']
                content = row['Contenu']
                
                # Nettoyer le contenu
                content = content.replace('ï¿½', 'é').replace('Ã¯Â¿Â½', 'é')
                
                # Insérer dans PostgreSQL
                cursor.execute(
                    "INSERT INTO public.articles (article_code, contenu) VALUES (%s, %s)",
                    (article_code, content)
                )
                loaded_count += 1
        
        connection.commit()
        print(f"✅ {loaded_count} articles chargés avec succès")
        
        # 4. Vérification finale
        cursor.execute("SELECT COUNT(*) FROM public.articles")
        final_count = cursor.fetchone()[0]
        print(f"✅ Vérification: {final_count} articles dans la table")
        
        # 5. Afficher quelques exemples
        print("\n📖 Exemples d'articles chargés:")
        cursor.execute("SELECT article_code, LEFT(contenu, 100) as contenu_preview FROM public.articles LIMIT 3")
        samples = cursor.fetchall()
        
        for article_code, contenu_preview in samples:
            print(f"   - {article_code}: {contenu_preview}...")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 Chargement terminé avec succès!")
        print("🌐 Vous pouvez maintenant utiliser l'API avec les données PostgreSQL")
        
    except FileNotFoundError:
        print("❌ Fichier articles_structures.csv non trouvé")
    except psycopg2.Error as e:
        print(f"❌ Erreur PostgreSQL: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    load_csv_to_postgres()
