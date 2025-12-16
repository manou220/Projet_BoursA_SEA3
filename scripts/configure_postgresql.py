#!/usr/bin/env python3
"""
Script interactif pour configurer PostgreSQL dans le fichier .env
Usage: python scripts/configure_postgresql.py
"""
import os
import sys
from pathlib import Path

def get_input(prompt, default=None, password=False):
    """Demande une entrée à l'utilisateur."""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    if password:
        import getpass
        value = getpass.getpass(prompt)
    else:
        value = input(prompt)
    
    return value.strip() if value.strip() else default

def build_database_url(host, port, database, user, password):
    """Construit l'URL de connexion PostgreSQL."""
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

def update_env_file(database_url):
    """Met à jour ou crée le fichier .env."""
    env_file = Path('.env')
    env_example = Path('ENV_EXAMPLE.txt')
    
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
    
    # Mettre à jour ou ajouter DATABASE_URL
    updated = False
    new_lines = []
    
    for line in lines:
        if line.startswith('DATABASE_URL=') or line.startswith('# DATABASE_URL='):
            new_lines.append(f"DATABASE_URL={database_url}\n")
            updated = True
        elif line.startswith('SQLALCHEMY_DATABASE_URI=') or line.startswith('# SQLALCHEMY_DATABASE_URI='):
            new_lines.append(f"SQLALCHEMY_DATABASE_URI={database_url}\n")
            updated = True
        else:
            new_lines.append(line)
    
    # Si DATABASE_URL n'existe pas, l'ajouter
    if not updated:
        # Chercher où insérer (après les commentaires de base de données)
        insert_index = len(new_lines)
        for i, line in enumerate(new_lines):
            if 'CONFIGURATION BASE DE DONNÉES' in line or 'BASE DE DONNÉES' in line:
                # Trouver la fin de la section
                for j in range(i+1, len(new_lines)):
                    if new_lines[j].strip() and not new_lines[j].startswith('#'):
                        insert_index = j
                        break
                break
        
        # Insérer les lignes
        new_lines.insert(insert_index, f"\n# Configuration PostgreSQL\n")
        new_lines.insert(insert_index + 1, f"DATABASE_URL={database_url}\n")
        new_lines.insert(insert_index + 2, f"SQLALCHEMY_DATABASE_URI={database_url}\n")
    
    # Écrire le fichier
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n[OK] Fichier .env mis a jour avec succes!")

def test_connection(database_url):
    """Teste la connexion à PostgreSQL."""
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        parsed = urlparse(database_url)
        
        print("\n" + "=" * 60)
        print("TEST DE CONNEXION")
        print("=" * 60)
        print("Tentative de connexion...")
        
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password
        )
        
        print("[OK] Connexion a PostgreSQL reussie!")
        
        # Lister les tables
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"[OK] {len(tables)} table(s) trouvee(s) dans la base:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("[ATTENTION] Aucune table trouvee")
        
        cursor.close()
        conn.close()
        
        print("=" * 60)
        print("[OK] TEST REUSSI!")
        print("=" * 60)
        return True
        
    except ImportError:
        print("\n[ERREUR] psycopg2 non installe")
        print("   Installez avec: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"\n[ERREUR] Erreur de connexion : {e}")
        print("\nVerifiez :")
        print("  - Que PostgreSQL est demarre")
        print("  - Que les informations sont correctes")
        print("  - Que la base de donnees existe")
        return False

def main():
    print("=" * 60)
    print("CONFIGURATION POSTGRESQL POUR LE PROJET")
    print("=" * 60)
    print("\nCe script va vous aider a configurer votre base PostgreSQL.")
    print("Vous aurez besoin de :")
    print("  - Host (localhost, IP, ou domaine)")
    print("  - Port (generalement 5432)")
    print("  - Nom de la base de donnees")
    print("  - Nom d'utilisateur")
    print("  - Mot de passe")
    print()
    
    # Demander les informations
    print("Entrez les informations de votre base PostgreSQL :")
    print()
    
    host = get_input("Host", "localhost")
    port = get_input("Port", "5432")
    database = get_input("Nom de la base de donnees")
    user = get_input("Nom d'utilisateur")
    password = get_input("Mot de passe", password=True)
    
    # Construire l'URL
    database_url = build_database_url(host, port, database, user, password)
    
    # Afficher un résumé (masquer le mot de passe)
    safe_url = database_url.split('@')[1] if '@' in database_url else database_url
    print(f"\n[INFO] URL de connexion : postgresql://***@{safe_url}")
    
    # Demander confirmation
    confirm = input("\nConfirmer cette configuration ? (o/n) [o]: ").strip().lower()
    if confirm and confirm != 'o':
        print("\n[INFO] Configuration annulee")
        return 1
    
    # Mettre à jour le fichier .env
    update_env_file(database_url)
    
    # Proposer de tester la connexion
    test = input("\nVoulez-vous tester la connexion maintenant ? (o/n) [o]: ").strip().lower()
    if not test or test == 'o':
        success = test_connection(database_url)
        if success:
            print("\n[OK] Configuration terminee avec succes!")
            print("\nProchaines etapes :")
            print("  1. Verifier la configuration : python scripts/check_config.py")
            print("  2. Initialiser les tables (si necessaire) : python scripts/init_db.py")
            print("  3. Tester l'application : python app_main.py")
            return 0
        else:
            print("\n[ATTENTION] La connexion a echoue, mais la configuration a ete sauvegardee.")
            print("  Verifiez vos informations et reessayez.")
            return 1
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[INFO] Configuration annulee par l'utilisateur")
        sys.exit(1)

