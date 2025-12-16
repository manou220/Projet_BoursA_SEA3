#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion réelle à MySQL.
Usage: python test_db_real_mysql.py
"""
import os
from dotenv import load_dotenv

load_dotenv()

try:
    import pymysql
    from urllib.parse import urlparse
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("[ERREUR] DATABASE_URL non configure dans .env")
        exit(1)
    
    if 'mysql' not in database_url:
        print("[ERREUR] DATABASE_URL ne semble pas etre MySQL")
        print(f"   Format actuel : {database_url[:30]}...")
        print("   Format attendu : mysql+pymysql://user:password@host:port/database")
        exit(1)
    
    # Parser l'URL (enlever mysql+pymysql://)
    url_clean = database_url.replace('mysql+pymysql://', 'mysql://')
    parsed = urlparse(url_clean)
    
    print("=" * 60)
    print("TEST DE CONNEXION MYSQL")
    print("=" * 60)
    print(f"Host : {parsed.hostname}")
    print(f"Port : {parsed.port or 3306}")
    print(f"Database : {parsed.path[1:] if parsed.path else 'N/A'}")
    print(f"User : {parsed.username}")
    print("-" * 60)
    
    # Connexion
    print("Tentative de connexion...")
    conn = pymysql.connect(
        host=parsed.hostname,
        port=parsed.port or 3306,
        database=parsed.path[1:],
        user=parsed.username,
        password=parsed.password
    )
    
    print("[OK] Connexion a MySQL reussie!")
    
    # Test simple
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION();")
    version = cursor.fetchone()
    print(f"[OK] Version MySQL : {version[0]}")
    
    # Lister les tables existantes
    cursor.execute("SHOW TABLES;")
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
    print("[ERREUR] pymysql non installe")
    print("   Installez avec: pip install pymysql")
    exit(1)
except pymysql.Error as e:
    print(f"[ERREUR] Erreur de connexion : {e}")
    print("\nVerifiez :")
    print("  - Que MySQL est demarre")
    print("  - Que le host et le port sont corrects")
    print("  - Que le nom d'utilisateur et le mot de passe sont corrects")
    print("  - Que la base de donnees existe")
    exit(1)
except Exception as e:
    print(f"[ERREUR] Erreur inattendue : {e}")
    exit(1)

