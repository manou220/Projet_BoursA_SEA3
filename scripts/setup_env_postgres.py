#!/usr/bin/env python3
"""
Script pour configurer automatiquement le fichier .env avec les informations PostgreSQL.
Usage: python scripts/setup_env_postgres.py
"""
import os
from pathlib import Path

# Vos informations PostgreSQL
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "ABOUAMAMBO"
POSTGRES_DATABASE = "BDD_BoursA"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"

# SECRET_KEY généré précédemment
SECRET_KEY = "bc574ed22f9a2918a41b82ab60f36945ff6c3f567fd2511d4f1bf0d20ba94f1f"

def setup_env_file():
    """Configure le fichier .env avec les informations PostgreSQL."""
    env_file = Path('.env')
    env_example = Path('ENV_EXAMPLE.txt')
    
    # Construire DATABASE_URL
    database_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    
    print("=" * 60)
    print("CONFIGURATION DU FICHIER .env")
    print("=" * 60)
    print(f"\nConfiguration PostgreSQL :")
    print(f"  Host : {POSTGRES_HOST}")
    print(f"  Port : {POSTGRES_PORT}")
    print(f"  Database : {POSTGRES_DATABASE}")
    print(f"  User : {POSTGRES_USER}")
    print(f"  URL : postgresql://{POSTGRES_USER}:***@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}")
    
    # Si .env n'existe pas, copier depuis ENV_EXAMPLE.txt
    if not env_file.exists():
        if env_example.exists():
            print("\n[INFO] Fichier .env n'existe pas, copie depuis ENV_EXAMPLE.txt...")
            with open(env_example, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print("\n[INFO] Creation d'un nouveau fichier .env...")
            env_file.touch()
    
    # Lire le contenu actuel
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Mettre à jour ou ajouter les variables
    updated_vars = {
        'DATABASE_URL': database_url,
        'SQLALCHEMY_DATABASE_URI': database_url,
        'SECRET_KEY': SECRET_KEY,
        'FLASK_ENV': 'production',
        'APP_CONFIG': 'production'
    }
    
    new_lines = []
    vars_found = {var: False for var in updated_vars.keys()}
    
    for line in lines:
        line_stripped = line.strip()
        updated = False
        
        for var_name, var_value in updated_vars.items():
            # Chercher la ligne avec cette variable (avec ou sans #)
            if line_stripped.startswith(f'{var_name}=') or line_stripped.startswith(f'# {var_name}='):
                new_lines.append(f"{var_name}={var_value}\n")
                vars_found[var_name] = True
                updated = True
                break
        
        if not updated:
            new_lines.append(line)
    
    # Ajouter les variables manquantes
    for var_name, var_value in updated_vars.items():
        if not vars_found[var_name]:
            # Trouver où insérer (après les sections de configuration)
            if var_name in ['DATABASE_URL', 'SQLALCHEMY_DATABASE_URI']:
                # Insérer dans la section BASE DE DONNÉES
                insert_index = len(new_lines)
                for i, line in enumerate(new_lines):
                    if 'CONFIGURATION BASE DE DONNÉES' in line or 'BASE DE DONNÉES' in line:
                        # Trouver la fin de la section
                        for j in range(i+1, len(new_lines)):
                            if new_lines[j].strip() and not new_lines[j].startswith('#'):
                                insert_index = j
                                break
                        break
                new_lines.insert(insert_index, f"{var_name}={var_value}\n")
            elif var_name == 'SECRET_KEY':
                # Insérer dans la section CONFIGURATION OBLIGATOIRE
                insert_index = len(new_lines)
                for i, line in enumerate(new_lines):
                    if 'CONFIGURATION OBLIGATOIRE' in line:
                        for j in range(i+1, len(new_lines)):
                            if 'SECRET_KEY' in new_lines[j] or (new_lines[j].strip() and not new_lines[j].startswith('#') and j > i + 5):
                                insert_index = j
                                break
                        break
                new_lines.insert(insert_index, f"{var_name}={var_value}\n")
            elif var_name in ['FLASK_ENV', 'APP_CONFIG']:
                # Insérer après SECRET_KEY ou dans la section ENVIRONNEMENT
                insert_index = len(new_lines)
                for i, line in enumerate(new_lines):
                    if 'Environnement Flask' in line or 'FLASK_ENV' in line:
                        insert_index = i + 1
                        break
                if insert_index == len(new_lines):
                    # Ajouter à la fin de la section CONFIGURATION OBLIGATOIRE
                    for i, line in enumerate(new_lines):
                        if 'CONFIGURATION OBLIGATOIRE' in line:
                            for j in range(i+1, len(new_lines)):
                                if new_lines[j].strip() and not new_lines[j].startswith('#') and '=' not in new_lines[j]:
                                    insert_index = j
                                    break
                            break
                new_lines.insert(insert_index, f"{var_name}={var_value}\n")
    
    # Écrire le fichier
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("\n[OK] Fichier .env configure avec succes!")
    print("\nVariables configurees :")
    for var_name in updated_vars.keys():
        print(f"  - {var_name}")
    
    return True

if __name__ == '__main__':
    try:
        setup_env_file()
        print("\n" + "=" * 60)
        print("ETAPES SUIVANTES :")
        print("=" * 60)
        print("1. Tester la connexion : python test_connection.py")
        print("2. Tester la connexion reelle : python test_db_real.py")
        print("3. Verifier la configuration : python scripts/check_config.py")
        print("=" * 60)
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()

