#!/usr/bin/env python3
"""
Script de migration de SQLite vers PostgreSQL.
Usage: python scripts/migrate_to_postgresql.py
"""

import os
import sys
import sqlite3
import psycopg2
from psycopg2.extras import execute_values
from urllib.parse import urlparse

def get_sqlite_data(db_path):
    """Récupère toutes les données de SQLite."""
    if not os.path.exists(db_path):
        print(f"❌ Fichier SQLite non trouvé: {db_path}")
        return None
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    data = {}
    
    # Récupérer les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        if table == 'sqlite_sequence':
            continue
        
        cursor.execute(f"SELECT * FROM {table}")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        data[table] = {
            'columns': columns,
            'rows': rows
        }
        print(f"✅ Table {table}: {len(rows)} lignes")
    
    conn.close()
    return data

def migrate_to_postgresql(sqlite_data, postgres_url):
    """Migre les données vers PostgreSQL."""
    parsed = urlparse(postgres_url)
    
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        database=parsed.path[1:],  # Enlever le '/'
        user=parsed.username,
        password=parsed.password
    )
    
    cursor = conn.cursor()
    
    for table_name, table_data in sqlite_data.items():
        if not table_data['rows']:
            print(f"⏭️  Table {table_name} vide, ignorée")
            continue
        
        columns = table_data['columns']
        rows = table_data['rows']
        
        # Créer la table si elle n'existe pas (structure basique)
        # Note: Ce script suppose que les tables existent déjà via SQLAlchemy
        # Sinon, il faudrait créer les tables ici
        
        # Insérer les données
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join([f'"{col}"' for col in columns])
        
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
        
        try:
            execute_values(cursor, query, rows, template=None, page_size=100)
            conn.commit()
            print(f"✅ Table {table_name}: {len(rows)} lignes migrées")
        except Exception as e:
            conn.rollback()
            print(f"❌ Erreur lors de la migration de {table_name}: {e}")
            print(f"   Vérifiez que la table existe et que le schéma correspond")
    
    cursor.close()
    conn.close()

def main():
    """Fonction principale."""
    print("🔄 Migration SQLite → PostgreSQL")
    print("=" * 50)
    
    # Vérifier les variables d'environnement
    sqlite_path = os.environ.get('SQLITE_DB_PATH', 'user_locations.db')
    postgres_url = os.environ.get('DATABASE_URL')
    
    if not postgres_url:
        print("❌ DATABASE_URL non défini")
        print("   Exemple: DATABASE_URL=postgresql://user:password@localhost:5432/dbname")
        sys.exit(1)
    
    if 'sqlite' in postgres_url.lower():
        print("❌ DATABASE_URL pointe vers SQLite, pas PostgreSQL")
        sys.exit(1)
    
    # Récupérer les données SQLite
    print(f"\n📦 Lecture de SQLite: {sqlite_path}")
    sqlite_data = get_sqlite_data(sqlite_path)
    
    if not sqlite_data:
        print("❌ Aucune donnée à migrer")
        sys.exit(1)
    
    # Migrer vers PostgreSQL
    print(f"\n🚀 Migration vers PostgreSQL...")
    migrate_to_postgresql(sqlite_data, postgres_url)
    
    print("\n✅ Migration terminée !")
    print("⚠️  Vérifiez les données dans PostgreSQL avant de supprimer SQLite")

if __name__ == '__main__':
    main()

