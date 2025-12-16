#!/usr/bin/env python3
"""
Vérifie que toutes les configurations sont en place pour le déploiement.
Usage: python scripts/check_config.py
"""
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("❌ python-dotenv n'est pas installé. Installez-le avec: pip install python-dotenv")
    sys.exit(1)

def check_file_exists(filepath):
    """Vérifie si un fichier existe."""
    return Path(filepath).exists()

def main():
    print("=" * 70)
    print("VÉRIFICATION DE LA CONFIGURATION POUR LE DÉPLOIEMENT")
    print("=" * 70)
    print()
    
    all_ok = True
    critical_checks = []
    important_checks = []
    
    # Vérifications critiques
    print("VERIFICATIONS CRITIQUES :")
    print("-" * 70)
    
    # Fichier .env
    env_file = Path('.env')
    if env_file.exists():
        print("[OK] Fichier .env existe")
    else:
        print("[ERREUR] Fichier .env MANQUANT - Creez-le depuis ENV_EXAMPLE.txt")
        all_ok = False
        critical_checks.append("Fichier .env")
    
    # DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Masquer le mot de passe
        if '@' in database_url:
            safe_url = database_url.split('@')[1] if '@' in database_url else database_url
            print(f"[OK] DATABASE_URL: Configure ({safe_url})")
        else:
            print(f"[OK] DATABASE_URL: Configure")
    else:
        print("[ERREUR] DATABASE_URL: MANQUANT - Obligatoire en production")
        all_ok = False
        critical_checks.append("DATABASE_URL")
    
    # SECRET_KEY
    secret_key = os.getenv('SECRET_KEY')
    if secret_key and secret_key != 'votre-cle-secrete-generee-ici-changez-moi':
        print(f"[OK] SECRET_KEY: Configure ({len(secret_key)} caracteres)")
    else:
        print("[ERREUR] SECRET_KEY: MANQUANT ou valeur par defaut - Generez-en une")
        all_ok = False
        critical_checks.append("SECRET_KEY")
    
    # FLASK_ENV
    flask_env = os.getenv('FLASK_ENV')
    if flask_env == 'production':
        print("[OK] FLASK_ENV: production")
    else:
        print(f"[ATTENTION] FLASK_ENV: {flask_env or 'non defini'} (devrait etre 'production')")
    
    print()
    
    # Vérifications importantes
    print("VERIFICATIONS IMPORTANTES :")
    print("-" * 70)
    
    # REDIS_PASSWORD
    redis_password = os.getenv('REDIS_PASSWORD')
    if redis_password and redis_password != 'changez-moi-en-production':
        print("[OK] REDIS_PASSWORD: Configure")
    else:
        print("[ATTENTION] REDIS_PASSWORD: Non configure ou valeur par defaut")
        important_checks.append("REDIS_PASSWORD")
    
    # POSTGRES_PASSWORD
    postgres_password = os.getenv('POSTGRES_PASSWORD')
    if postgres_password and postgres_password != 'changez-moi-en-production':
        print("[OK] POSTGRES_PASSWORD: Configure")
    else:
        print("[ATTENTION] POSTGRES_PASSWORD: Non configure ou valeur par defaut (si PostgreSQL dans Docker)")
    
    # Certificats SSL
    cert_path = Path('nginx/ssl/cert.pem')
    key_path = Path('nginx/ssl/key.pem')
    if cert_path.exists() and key_path.exists():
        print("[OK] Certificats SSL: Presents")
    else:
        print("[ERREUR] Certificats SSL: MANQUANTS (nginx/ssl/cert.pem et key.pem)")
        important_checks.append("Certificats SSL")
    
    # Répertoire nginx/ssl
    ssl_dir = Path('nginx/ssl')
    if ssl_dir.exists():
        print("[OK] Repertoire nginx/ssl: Existe")
    else:
        print("[ATTENTION] Repertoire nginx/ssl: N'existe pas (sera cree avec les certificats)")
    
    print()
    
    # Résumé
    print("=" * 70)
    if all_ok and len(important_checks) == 0:
        print("[OK] TOUTES LES CONFIGURATIONS SONT EN PLACE!")
        print("   Vous pouvez proceder au deploiement.")
    elif all_ok:
        print("[OK] CONFIGURATIONS CRITIQUES OK")
        print(f"[ATTENTION] {len(important_checks)} element(s) important(s) a verifier:")
        for check in important_checks:
            print(f"   - {check}")
    else:
        print("[ERREUR] CONFIGURATIONS MANQUANTES")
        print(f"   {len(critical_checks)} element(s) critique(s) manquant(s):")
        for check in critical_checks:
            print(f"   - {check}")
        if important_checks:
            print(f"\n   {len(important_checks)} element(s) important(s) a verifier:")
            for check in important_checks:
                print(f"   - {check}")
        print("\n   Consultez CHECKLIST_DEPLOIEMENT_FINALE.md pour les instructions.")
    print("=" * 70)
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())

