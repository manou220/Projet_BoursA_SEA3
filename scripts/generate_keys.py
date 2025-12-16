#!/usr/bin/env python3
"""
Génère toutes les clés nécessaires pour le déploiement.
Usage: python scripts/generate_keys.py
"""
import secrets

def main():
    print("=" * 60)
    print("GÉNÉRATION DES CLÉS POUR LE DÉPLOIEMENT")
    print("=" * 60)
    print()
    
    secret_key = secrets.token_hex(32)
    redis_password = secrets.token_urlsafe(32)
    postgres_password = secrets.token_urlsafe(32)
    
    print("# Ajoutez ces lignes dans votre fichier .env :")
    print()
    print(f"SECRET_KEY={secret_key}")
    print(f"REDIS_PASSWORD={redis_password}")
    print(f"POSTGRES_PASSWORD={postgres_password}")
    print()
    print("=" * 60)
    print("IMPORTANT :")
    print("   - Copiez ces valeurs dans votre fichier .env")
    print("   - Ne partagez JAMAIS ces cles")
    print("   - Ne commitez JAMAIS le fichier .env dans Git")
    print("=" * 60)

if __name__ == '__main__':
    main()

