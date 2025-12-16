#!/usr/bin/env python3
"""
Script pour générer le fichier .env avec des valeurs sécurisées.
Usage: python scripts/generate_env.py
"""
import os
import secrets
import sys

def generate_secret_key():
    """Génère une clé secrète Flask sécurisée."""
    return secrets.token_hex(32)

def generate_password():
    """Génère un mot de passe sécurisé."""
    return secrets.token_urlsafe(24)

def create_env_file():
    """Crée le fichier .env avec des valeurs sécurisées."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    
    if os.path.exists(env_path):
        print(f"Le fichier .env existe deja a {env_path}.")
        response = input("Voulez-vous le remplacer? (o/N): ")
        if response.lower() != 'o':
            print("Operation annulee.")
            return False
    
    # Générer les valeurs sécurisées
    secret_key = generate_secret_key()
    redis_password = generate_password()
    postgres_password = generate_password()
    
    env_content = f"""# ============================================
# Configuration de l'application BoursA
# ============================================
# Fichier généré automatiquement - Vérifiez et modifiez les valeurs si nécessaire
# IMPORTANT: Ne commitez JAMAIS ce fichier dans le repository

# ============================================
# CONFIGURATION OBLIGATOIRE EN PRODUCTION
# ============================================

# Clé secrète Flask (OBLIGATOIRE en production)
# Générée automatiquement - CONSERVEZ CETTE VALEUR SECRÈTE
SECRET_KEY={secret_key}

# Environnement Flask (development, production, testing)
FLASK_ENV=production

# Configuration de l'application
APP_CONFIG=production

# ============================================
# CONFIGURATION REDIS (Recommandé en production)
# ============================================

# Type de cache (SimpleCache pour dev, Redis pour production)
CACHE_TYPE=Redis

# URL Redis complète (format: redis://:password@host:port/db)
# Pour Docker Compose, sera construit automatiquement depuis REDIS_PASSWORD
# CACHE_REDIS_URL=redis://:{redis_password}@localhost:6379/0

# ============================================
# CONFIGURATION BASE DE DONNÉES
# ============================================

# Variables PostgreSQL pour Docker Compose (OBLIGATOIRES)
POSTGRES_DB=boursa
POSTGRES_USER=boursa_user
POSTGRES_PASSWORD={postgres_password}

# ============================================
# CONFIGURATION SÉCURITÉ
# ============================================

# Désactiver l'inscription publique (recommandé en production)
DISABLE_PUBLIC_REGISTRATION=false

# Limites de connexion
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_DURATION=30

# ============================================
# CONFIGURATION APIs BOURSIÈRES (Optionnel)
# ============================================

# Clé API Alpha Vantage (optionnel)
# ALPHAVANTAGE_KEY=votre-cle-alpha-vantage

# Clé API IEX Cloud (optionnel)
# IEX_CLOUD_API_KEY=votre-cle-iex-cloud

# ============================================
# CONFIGURATION LOGGING
# ============================================

# Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Fichier de log (None = console seulement)
LOG_FILE=logs/app.log

# ============================================
# CONFIGURATION DOCKER COMPOSE (si utilisé)
# ============================================

# Mot de passe Redis pour Docker Compose (OBLIGATOIRE)
REDIS_PASSWORD={redis_password}
"""
    
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"Fichier .env cree avec succes: {env_path}")
        print("\nValeurs generees:")
        print(f"   SECRET_KEY: {secret_key[:20]}...")
        print(f"   REDIS_PASSWORD: {redis_password[:20]}...")
        print(f"   POSTGRES_PASSWORD: {postgres_password[:20]}...")
        print("\nIMPORTANT: Conservez ces valeurs en securite!")
        print("   Le fichier .env est deja dans .gitignore et ne sera pas commite.")
        
        return True
    except Exception as e:
        print(f"Erreur lors de la creation du fichier .env: {e}")
        return False

if __name__ == '__main__':
    success = create_env_file()
    sys.exit(0 if success else 1)

