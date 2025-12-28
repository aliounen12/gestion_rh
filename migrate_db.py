#!/usr/bin/env python3
"""
Script pour migrer les données vers une nouvelle base PostgreSQL (Supabase/Neon)
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import sys
import os

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Ancienne base (source) - À MODIFIER
OLD_DB = {
    "host": os.getenv("OLD_DB_HOST", "localhost"),
    "port": int(os.getenv("OLD_DB_PORT", "5432")),
    "database": os.getenv("OLD_DB_NAME", "ancien_db"),
    "user": os.getenv("OLD_DB_USER", "postgres"),
    "password": os.getenv("OLD_DB_PASSWORD", "")
}

# Nouvelle base (destination - Supabase/Neon) - À MODIFIER
NEW_DB = {
    "host": os.getenv("NEW_DB_HOST", "db.xxxxx.supabase.co"),
    "port": int(os.getenv("NEW_DB_PORT", "5432")),
    "database": os.getenv("NEW_DB_NAME", "postgres"),
    "user": os.getenv("NEW_DB_USER", "postgres"),
    "password": os.getenv("NEW_DB_PASSWORD", "")
}

def migrate_table(conn_old, conn_new, table_name):
    """Migre une table de l'ancienne vers la nouvelle base"""
    cursor_old = conn_old.cursor(cursor_factory=RealDictCursor)
    cursor_new = conn_new.cursor()
    
    try:
        # Récupérer les données
        cursor_old.execute(f"SELECT * FROM {table_name} ORDER BY 1")
        rows = cursor_old.fetchall()
        
        if not rows:
            print(f"⚠️  Aucune donnée dans {table_name}")
            return
        
        print(f"\n📦 Migration de {len(rows)} lignes de {table_name}...")
        
        # Récupérer les colonnes
        columns = list(rows[0].keys())
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))
        
        # Compter les insertions
        inserted = 0
        skipped = 0
        
        # Insérer dans la nouvelle base
        for row in rows:
            values = tuple(row[col] for col in columns)
            
            # Utiliser ON CONFLICT pour éviter les doublons
            if table_name == "public.sujet":
                conflict = "ON CONFLICT (id) DO NOTHING"
            elif table_name == "public.article":
                conflict = "ON CONFLICT (article_id) DO NOTHING"
            else:
                conflict = "ON CONFLICT DO NOTHING"
            
            query = f"""
                INSERT INTO {table_name} ({columns_str}) 
                VALUES ({placeholders}) 
                {conflict}
            """
            
            cursor_new.execute(query, values)
            if cursor_new.rowcount > 0:
                inserted += 1
            else:
                skipped += 1
        
        conn_new.commit()
        print(f"✅ {table_name}: {inserted} insérés, {skipped} ignorés (doublons)")
        
    except Exception as e:
        conn_new.rollback()
        print(f"❌ Erreur lors de la migration de {table_name}: {e}")
        raise
    finally:
        cursor_old.close()
        cursor_new.close()

def main():
    """Fonction principale de migration"""
    print("=" * 60)
    print("🚀 Script de migration PostgreSQL")
    print("=" * 60)
    
    # Vérifier les connexions
    print("\n1. Test de connexion à l'ancienne base...")
    try:
        conn_old = psycopg2.connect(**OLD_DB)
        print("✅ Connexion à l'ancienne base réussie")
    except Exception as e:
        print(f"❌ Erreur de connexion à l'ancienne base: {e}")
        print("\n💡 Vérifiez vos variables d'environnement:")
        print("   - OLD_DB_HOST, OLD_DB_PORT, OLD_DB_NAME, OLD_DB_USER, OLD_DB_PASSWORD")
        sys.exit(1)
    
    print("\n2. Test de connexion à la nouvelle base...")
    try:
        conn_new = psycopg2.connect(**NEW_DB)
        print("✅ Connexion à la nouvelle base réussie")
    except Exception as e:
        print(f"❌ Erreur de connexion à la nouvelle base: {e}")
        print("\n💡 Vérifiez vos variables d'environnement:")
        print("   - NEW_DB_HOST, NEW_DB_PORT, NEW_DB_NAME, NEW_DB_USER, NEW_DB_PASSWORD")
        conn_old.close()
        sys.exit(1)
    
    # Migrer les tables
    print("\n3. Début de la migration...")
    try:
        # Migrer d'abord les sujets (table parent)
        migrate_table(conn_old, conn_new, "public.sujet")
        
        # Puis les articles (table enfant)
        migrate_table(conn_old, conn_new, "public.article")
        
        print("\n" + "=" * 60)
        print("✅ Migration terminée avec succès !")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ Erreur lors de la migration: {e}")
        print("=" * 60)
        sys.exit(1)
    finally:
        conn_old.close()
        conn_new.close()

if __name__ == "__main__":
    main()
