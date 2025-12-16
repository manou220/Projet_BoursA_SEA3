#!/usr/bin/env python3
"""
Script de vérification complète pour la production.
Vérifie tous les éléments qui pourraient empêcher l'application de tourner en production.
Usage: python scripts/check_production_readiness.py
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

def check_critical_config():
    """Vérifie les configurations critiques."""
    print("=" * 70)
    print("VERIFICATION DES CONFIGURATIONS CRITIQUES")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        issues.append("DATABASE_URL non configure - OBLIGATOIRE en production")
    elif 'sqlite' in database_url.lower():
        issues.append("DATABASE_URL utilise SQLite - PostgreSQL requis en production")
    else:
        print("[OK] DATABASE_URL configure avec PostgreSQL")
    
    # SECRET_KEY
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key or secret_key == 'dev-secret-key-change-in-production' or secret_key == 'votre-cle-secrete-generee-ici-changez-moi':
        issues.append("SECRET_KEY non configure ou valeur par defaut - OBLIGATOIRE en production")
    else:
        print("[OK] SECRET_KEY configure")
    
    # FLASK_ENV
    flask_env = os.getenv('FLASK_ENV')
    if flask_env != 'production':
        warnings.append(f"FLASK_ENV={flask_env} (devrait etre 'production')")
    else:
        print("[OK] FLASK_ENV=production")
    
    # Redis
    redis_url = os.getenv('CACHE_REDIS_URL')
    if not redis_url:
        warnings.append("CACHE_REDIS_URL non configure - SimpleCache sera utilise (non optimal pour plusieurs instances)")
    else:
        print("[OK] CACHE_REDIS_URL configure")
    
    return issues, warnings

def check_dependencies():
    """Vérifie les dépendances critiques."""
    print("\n" + "=" * 70)
    print("VERIFICATION DES DEPENDANCES")
    print("=" * 70)
    
    issues = []
    warnings = []
    critical_deps = {
        'flask': 'Flask',
        'sqlalchemy': 'SQLAlchemy',
        'psycopg2': 'psycopg2-binary (PostgreSQL)',
        'gunicorn': 'gunicorn (serveur WSGI)',
        'redis': 'redis (pour cache)',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'flask_login': 'Flask-Login',
        'flask_caching': 'Flask-Caching',
    }
    
    for module, name in critical_deps.items():
        try:
            __import__(module)
            print(f"[OK] {name} installe")
        except ImportError:
            if module in ['psycopg2', 'redis']:
                warnings.append(f"{name} non installe (optionnel mais recommande)")
            else:
                issues.append(f"{name} non installe - OBLIGATOIRE")
    
    return issues, warnings

def check_files_and_directories():
    """Vérifie les fichiers et répertoires nécessaires."""
    print("\n" + "=" * 70)
    print("VERIFICATION DES FICHIERS ET REPERTOIRES")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # Fichiers critiques
    critical_files = {
        '.env': 'Fichier de configuration',
        'wsgi.py': 'Point d\'entree WSGI',
        'app/__init__.py': 'Module principal de l\'application',
        'app/config.py': 'Configuration de l\'application',
    }
    
    for file_path, description in critical_files.items():
        if Path(file_path).exists():
            print(f"[OK] {description} existe")
        else:
            issues.append(f"{description} manquant: {file_path}")
    
    # Répertoires nécessaires
    required_dirs = ['uploads', 'logs', 'app/templates', 'app/static']
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"[OK] Repertoire {dir_path} existe")
        else:
            warnings.append(f"Repertoire {dir_path} n'existe pas (sera cree automatiquement)")
    
    # Certificats SSL
    cert_path = Path('nginx/ssl/cert.pem')
    key_path = Path('nginx/ssl/key.pem')
    if cert_path.exists() and key_path.exists():
        print("[OK] Certificats SSL presents")
    else:
        warnings.append("Certificats SSL manquants (nginx/ssl/cert.pem et key.pem) - Necessaire pour HTTPS")
    
    return issues, warnings

def check_code_issues():
    """Vérifie les problèmes potentiels dans le code."""
    print("\n" + "=" * 70)
    print("VERIFICATION DU CODE")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # Vérifier app/__init__.py pour les chemins hardcodés
    init_file = Path('app/__init__.py')
    if init_file.exists():
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'user_locations.db' in content:
                warnings.append("Reference a user_locations.db dans app/__init__.py (normal si fallback SQLite)")
    
    # Vérifier ProductionConfig
    config_file = Path('app/config.py')
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'SESSION_COOKIE_SECURE = True' in content:
                print("[OK] SESSION_COOKIE_SECURE active en production")
            else:
                warnings.append("SESSION_COOKIE_SECURE non active en production")
    
    return issues, warnings

def check_database_connection():
    """Teste la connexion à la base de données."""
    print("\n" + "=" * 70)
    print("VERIFICATION DE LA CONNEXION BASE DE DONNEES")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        issues.append("Impossible de tester la connexion - DATABASE_URL non configure")
        return issues, warnings
    
    try:
        from urllib.parse import urlparse
        parsed = urlparse(database_url)
        
        if 'postgresql' in database_url:
            try:
                import psycopg2
                conn = psycopg2.connect(
                    host=parsed.hostname,
                    port=parsed.port or 5432,
                    database=parsed.path[1:],
                    user=parsed.username,
                    password=parsed.password
                )
                
                # Vérifier les tables
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
                tables = [row[0] for row in cursor.fetchall()]
                
                required_tables = ['users', 'data_files', 'test_history', 'user_locations']
                missing_tables = [t for t in required_tables if t not in tables]
                
                if missing_tables:
                    warnings.append(f"Tables manquantes: {', '.join(missing_tables)}")
                else:
                    print(f"[OK] Connexion PostgreSQL reussie - {len(tables)} tables trouvees")
                
                cursor.close()
                conn.close()
                
            except ImportError:
                issues.append("psycopg2 non installe - Impossible de tester la connexion PostgreSQL")
            except Exception as e:
                issues.append(f"Erreur de connexion PostgreSQL: {e}")
        else:
            warnings.append("Type de base de donnees non PostgreSQL - test non effectue")
            
    except Exception as e:
        warnings.append(f"Erreur lors du test de connexion: {e}")
    
    return issues, warnings

def check_security():
    """Vérifie les aspects de sécurité."""
    print("\n" + "=" * 70)
    print("VERIFICATION DE LA SECURITE")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # SECRET_KEY
    secret_key = os.getenv('SECRET_KEY')
    if secret_key and len(secret_key) < 32:
        warnings.append("SECRET_KEY trop court (minimum 32 caracteres recommande)")
    else:
        print("[OK] SECRET_KEY de longueur adequate")
    
    # DEBUG mode
    debug = os.getenv('FLASK_DEBUG', 'False').lower()
    if debug == 'true':
        issues.append("FLASK_DEBUG=True - DESACTIVEZ en production!")
    else:
        print("[OK] DEBUG mode desactive")
    
    # HTTPS
    flask_env = os.getenv('FLASK_ENV')
    if flask_env == 'production':
        cert_path = Path('nginx/ssl/cert.pem')
        if not cert_path.exists():
            warnings.append("Certificats SSL manquants - HTTPS ne fonctionnera pas")
        else:
            print("[OK] Certificats SSL presents")
    
    return issues, warnings

def main():
    """Fonction principale."""
    print("\n" + "=" * 70)
    print("VERIFICATION COMPLETE POUR LA PRODUCTION")
    print("=" * 70)
    print()
    
    all_issues = []
    all_warnings = []
    
    # Vérifications
    issues, warnings = check_critical_config()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_dependencies()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_files_and_directories()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_code_issues()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_database_connection()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_security()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    # Résumé
    print("\n" + "=" * 70)
    print("RESUME")
    print("=" * 70)
    
    if not all_issues and not all_warnings:
        print("[OK] AUCUN PROBLEME DETECTE - Application prete pour la production!")
        return 0
    elif not all_issues:
        print(f"[OK] CONFIGURATIONS CRITIQUES OK")
        print(f"[ATTENTION] {len(all_warnings)} element(s) a verifier:")
        for warning in all_warnings:
            print(f"  - {warning}")
        return 0
    else:
        print(f"[ERREUR] {len(all_issues)} probleme(s) critique(s) detecte(s):")
        for issue in all_issues:
            print(f"  - {issue}")
        
        if all_warnings:
            print(f"\n[ATTENTION] {len(all_warnings)} element(s) a verifier:")
            for warning in all_warnings:
                print(f"  - {warning}")
        
        print("\n[INFO] Corrigez les problemes critiques avant le deploiement en production")
        return 1

if __name__ == '__main__':
    sys.exit(main())

