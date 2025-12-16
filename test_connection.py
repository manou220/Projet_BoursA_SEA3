#!/usr/bin/env python3
"""
Script de test simple pour vérifier que DATABASE_URL est configuré.
Usage: python test_connection.py
"""
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv('DATABASE_URL')
if database_url:
    print("[OK] DATABASE_URL trouve")
    # Masquer le mot de passe
    if '@' in database_url:
        safe_url = database_url.split('@')[1]
        print(f"   Connexion a : {safe_url}")
    else:
        print(f"   Format : {database_url[:50]}...")
    
    # Identifier le type
    if 'postgresql://' in database_url:
        print("   Type : PostgreSQL")
    elif 'mysql' in database_url:
        print("   Type : MySQL/MariaDB")
    elif 'sqlite' in database_url:
        print("   Type : SQLite")
    else:
        print("   Type : Inconnu")
else:
    print("[ERREUR] DATABASE_URL non trouve dans .env")
    print("   Ajoutez DATABASE_URL dans votre fichier .env")

