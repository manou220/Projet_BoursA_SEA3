#!/usr/bin/env python3
"""
Script interactif pour configurer la base de données SQL.
Guide l'utilisateur à travers la configuration de DATABASE_URL.
"""
import os
import sys
import re
from pathlib import Path

# Couleurs pour l'affichage
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def get_env_file_path():
    """Retourne le chemin du fichier .env"""
    project_root = Path(__file__).parent.parent
    return project_root / '.env'

def read_env_file():
    """Lit le fichier .env et retourne un dictionnaire"""
    env_path = get_env_file_path()
    env_vars = {}
    
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignorer les commentaires et lignes vides
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    
    return env_vars

def write_env_file(env_vars):
    """Écrit les variables d'environnement dans le fichier .env"""
    env_path = get_env_file_path()
    
    # Lire le contenu existant pour préserver les commentaires
    existing_content = []
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            existing_content = f.readlines()
    
    # Créer un dictionnaire des variables existantes
    existing_vars = {}
    new_content = []
    
    for line in existing_content:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and '=' in stripped:
            key = stripped.split('=', 1)[0].strip()
            existing_vars[key] = line
        else:
            new_content.append(line)
    
    # Mettre à jour ou ajouter les nouvelles variables
    for key, value in env_vars.items():
        if key in existing_vars:
            # Remplacer la ligne existante
            new_content = [line if not line.strip().startswith(key + '=') 
                          else f"{key}={value}\n" for line in new_content]
            if not any(line.strip().startswith(key + '=') for line in new_content):
                new_content.append(f"{key}={value}\n")
        else:
            # Ajouter à la fin
            new_content.append(f"{key}={value}\n")
    
    # Écrire le fichier
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(new_content)

def ask_database_type():
    """Demande le type de base de données"""
    print_header("Type de Base de Données")
    print("Quel type de base de données utilisez-vous ?")
    print("1. PostgreSQL (recommandé)")
    print("2. MySQL/MariaDB")
    
    while True:
        choice = input("\nVotre choix (1 ou 2): ").strip()
        if choice == '1':
            return 'postgresql'
        elif choice == '2':
            return 'mysql'
        else:
            print_error("Veuillez choisir 1 ou 2")

def ask_database_info(db_type):
    """Demande les informations de connexion à la base de données"""
    print_header("Informations de Connexion")
    
    print_info("Veuillez fournir les informations de connexion à votre base de données :")
    
    # Host
    default_host = 'localhost'
    host = input(f"\n📍 Host [{default_host}]: ").strip() or default_host
    
    # Port
    default_port = '5432' if db_type == 'postgresql' else '3306'
    while True:
        port = input(f"🔌 Port [{default_port}]: ").strip() or default_port
        try:
            port = int(port)
            if 1 <= port <= 65535:
                break
            else:
                print_error("Le port doit être entre 1 et 65535")
        except ValueError:
            print_error("Le port doit être un nombre")
    
    # Database name
    database = input("🗄️  Nom de la base de données: ").strip()
    if not database:
        print_error("Le nom de la base de données est obligatoire")
        sys.exit(1)
    
    # Username
    username = input("👤 Nom d'utilisateur: ").strip()
    if not username:
        print_error("Le nom d'utilisateur est obligatoire")
        sys.exit(1)
    
    # Password
    import getpass
    password = getpass.getpass("🔐 Mot de passe: ").strip()
    if not password:
        print_warning("Aucun mot de passe fourni (peut être valide pour certaines configurations)")
    
    return {
        'host': host,
        'port': str(port),
        'database': database,
        'username': username,
        'password': password
    }

def build_database_url(db_type, db_info):
    """Construit l'URL de la base de données"""
    if db_type == 'postgresql':
        url = f"postgresql://{db_info['username']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/{db_info['database']}"
    else:  # mysql
        url = f"mysql+pymysql://{db_info['username']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/{db_info['database']}"
    
    return url

def test_connection(database_url):
    """Teste la connexion à la base de données"""
    print_header("Test de Connexion")
    
    try:
        # Importer les modules nécessaires
        from app import create_app
        from app.extensions import db
        
        # Créer l'application avec la nouvelle URL
        os.environ['DATABASE_URL'] = database_url
        os.environ['SQLALCHEMY_DATABASE_URI'] = database_url
        
        app = create_app()
        
        with app.app_context():
            # Test de connexion
            result = db.session.execute(db.text('SELECT 1')).scalar()
            
            if result == 1:
                print_success("Connexion à la base de données réussie !")
                
                # Afficher les informations (sans mot de passe)
                safe_url = re.sub(r':([^:@]+)@', r':***@', database_url)
                print_info(f"Base de données: {safe_url}")
                
                # Lister les tables existantes
                try:
                    inspector = db.inspect(db.engine)
                    tables = inspector.get_table_names()
                    print_info(f"Tables existantes: {len(tables)}")
                    if tables:
                        for table in tables:
                            print(f"   - {table}")
                except Exception as e:
                    print_warning(f"Impossible de lister les tables: {e}")
                
                return True
            else:
                print_error("La connexion a échoué")
                return False
                
    except ImportError as e:
        print_error(f"Module manquant: {e}")
        if 'psycopg2' in str(e):
            print_info("Installez avec: pip install psycopg2-binary")
        elif 'pymysql' in str(e):
            print_info("Installez avec: pip install pymysql")
        return False
    except Exception as e:
        print_error(f"Erreur de connexion: {e}")
        print_info("Vérifiez que:")
        print("  - Le serveur de base de données est démarré")
        print("  - Les informations de connexion sont correctes")
        print("  - Le port est accessible")
        print("  - La base de données existe")
        return False

def ask_initialize_tables():
    """Demande si l'utilisateur veut initialiser les tables"""
    print_header("Initialisation des Tables")
    
    print("Voulez-vous créer les tables nécessaires maintenant ?")
    print("(Les tables seront créées si elles n'existent pas déjà)")
    
    while True:
        choice = input("\nInitialiser les tables ? (o/n) [o]: ").strip().lower() or 'o'
        if choice in ['o', 'oui', 'y', 'yes']:
            return True
        elif choice in ['n', 'non', 'no']:
            return False
        else:
            print_error("Veuillez répondre 'o' ou 'n'")

def initialize_tables():
    """Initialise les tables de la base de données"""
    print_header("Création des Tables")
    
    try:
        # Ajouter le répertoire parent au path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        
        from scripts.init_db import init_database
        
        if init_database():
            print_success("Tables initialisées avec succès !")
            return True
        else:
            print_error("Erreur lors de l'initialisation des tables")
            return False
            
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print_header("Configuration de la Base de Données SQL")
    
    print_info("Ce script va vous aider à configurer votre base de données SQL.")
    print_info("Vous aurez besoin des informations suivantes :")
    print("  - Type de base de données (PostgreSQL ou MySQL)")
    print("  - Host (adresse du serveur)")
    print("  - Port")
    print("  - Nom de la base de données")
    print("  - Nom d'utilisateur")
    print("  - Mot de passe")
    
    input("\nAppuyez sur Entrée pour continuer...")
    
    # Lire les variables existantes
    env_vars = read_env_file()
    
    # Demander le type de base de données
    db_type = ask_database_type()
    
    # Demander les informations
    db_info = ask_database_info(db_type)
    
    # Construire l'URL
    database_url = build_database_url(db_type, db_info)
    
    # Afficher l'URL (sans mot de passe)
    safe_url = re.sub(r':([^:@]+)@', r':***@', database_url)
    print_info(f"\nURL de la base de données: {safe_url}")
    
    # Tester la connexion
    if not test_connection(database_url):
        print_error("\nLa connexion a échoué. Vérifiez vos informations.")
        retry = input("\nVoulez-vous réessayer ? (o/n) [n]: ").strip().lower() or 'n'
        if retry in ['o', 'oui', 'y', 'yes']:
            return main()  # Recommencer
        else:
            print_info("Configuration annulée.")
            sys.exit(1)
    
    # Sauvegarder dans .env
    print_header("Sauvegarde de la Configuration")
    
    env_vars['DATABASE_URL'] = database_url
    env_vars['SQLALCHEMY_DATABASE_URI'] = database_url
    
    # S'assurer que FLASK_ENV est en production
    if 'FLASK_ENV' not in env_vars or env_vars['FLASK_ENV'] != 'production':
        env_vars['FLASK_ENV'] = 'production'
        print_info("FLASK_ENV défini sur 'production'")
    
    if 'APP_CONFIG' not in env_vars or env_vars['APP_CONFIG'] != 'production':
        env_vars['APP_CONFIG'] = 'production'
        print_info("APP_CONFIG défini sur 'production'")
    
    write_env_file(env_vars)
    print_success("Configuration sauvegardée dans .env")
    
    # Demander l'initialisation des tables
    if ask_initialize_tables():
        if initialize_tables():
            print_success("\n✅ Configuration terminée avec succès !")
        else:
            print_warning("\n⚠️  Configuration sauvegardée mais erreur lors de l'initialisation des tables.")
            print_info("Vous pouvez exécuter manuellement: python scripts/init_db.py")
    else:
        print_info("\nVous pouvez initialiser les tables plus tard avec: python scripts/init_db.py")
    
    print_header("Prochaines Étapes")
    print("1. Vérifiez la configuration avec: python scripts/init_db.py")
    print("2. Testez l'application avec: python app_main.py")
    print("3. Vérifiez le health check: curl http://localhost/health")
    print("\n✅ Configuration terminée !")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nConfiguration annulée par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print_error(f"\nErreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

