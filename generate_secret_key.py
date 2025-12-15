#!/usr/bin/env python3
"""
Script pour générer une clé secrète sécurisée pour Flask.
Utilisation: python generate_secret_key.py
"""

import secrets

def generate_secret_key():
    """Génère une clé secrète sécurisée de 64 caractères hexadécimaux."""
    return secrets.token_hex(32)

if __name__ == '__main__':
    secret_key = generate_secret_key()
    print("=" * 60)
    print("Clé secrète générée:")
    print("=" * 60)
    print(secret_key)
    print("=" * 60)
    print("\nAjoutez cette ligne dans votre fichier .env:")
    print(f"SECRET_KEY={secret_key}")
    print("\n⚠️  IMPORTANT: Ne partagez jamais cette clé publiquement!")
    print("=" * 60)

