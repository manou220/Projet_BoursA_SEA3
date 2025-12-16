#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion réelle à PostgreSQL.
Usage: python test_db_real.py
"""
import os
from dotenv import load_dotenv

load_dotenv()

try:
    import psycopg2
    from urllib.parse import urlparse
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("[ERREUR] DATABASE_URL non configure dans .env")
        exit(1)
    
    if 'postgresql://' not in database_url:
        print("[ERREUR] DATABASE_URL ne semble pas etre PostgreSQL")
        print(f"   Format actuel : {database_url[:30]}...")
        print("   Format attendu : postgresql://user:password@host:port/database")
        exit(1)
    
    # Parser l'URL
    parsed = urlparse(database_url)
    
    print("=" * 60)
    print("TEST DE CONNEXION POSTGRESQL")
    print("=" * 60)
    print(f"Host : {parsed.hostname}")
    print(f"Port : {parsed.port or 5432}")
    print(f"Database : {parsed.path[1:] if parsed.path else 'N/A'}")
    print(f"User : {parsed.username}")
    print("-" * 60)
    
    # Connexion
    print("Tentative de connexion...")
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        database=parsed.path[1:],  # Enlever le premier /
        user=parsed.username,
        password=parsed.password
    )
    
    print("[OK] Connexion a PostgreSQL reussie!")
    
    # Test simple
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"[OK] Version PostgreSQL : {version[0][:60]}...")
    
    # Lister les tables existantes
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    
    if tables:
        print(f"[OK] {len(tables)} table(s) trouvee(s) :")
        for table in tables:
            print(f"   - {table[0]}")
    else:
        print("[ATTENTION] Aucune table trouvee (normal si pas encore initialise)")
    
    cursor.close()
    conn.close()
    
    print("=" * 60)
    print("[OK] TEST REUSSI - La connexion fonctionne!")
    print("=" * 60)
    
except ImportError:
    print("[ERREUR] psycopg2 non installe")
    print("   Installez avec: pip install psycopg2-binary")
    exit(1)
except psycopg2.OperationalError as e:
    print(f"[ERREUR] Erreur de connexion : {e}")
    print("\nVerifiez :")
    print("  - Que PostgreSQL est demarre")
    print("  - Que le host et le port sont corrects")
    print("  - Que le nom d'utilisateur et le mot de passe sont corrects")
    print("  - Que la base de donnees existe")
    exit(1)
except Exception as e:
    print(f"[ERREUR] Erreur inattendue : {e}")
    exit(1)

