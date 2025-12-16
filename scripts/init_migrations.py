#!/usr/bin/env python3
"""
Script pour initialiser Flask-Migrate.
Usage: python scripts/init_migrations.py
"""
import os
import sys

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from flask_migrate import init, migrate, upgrade

def init_migrations():
    """Initialise Flask-Migrate et crée la première migration."""
    app = create_app()
    
    with app.app_context():
        print("🔧 Initialisation de Flask-Migrate...")
        
        migrations_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'migrations')
        
        # Initialiser Flask-Migrate si pas déjà fait
        if not os.path.exists(migrations_dir):
            print("📦 Création du répertoire migrations...")
            init()
            print("✅ Répertoire migrations créé")
        else:
            print("ℹ️  Le répertoire migrations existe déjà")
        
        # Créer la migration initiale
        print("📝 Création de la migration initiale...")
        try:
            migrate(message="Initial migration")
            print("✅ Migration créée")
        except Exception as e:
            print(f"⚠️  Erreur lors de la création de la migration: {e}")
            print("   Cela peut être normal si les migrations existent déjà")
        
        # Appliquer les migrations
        print("🚀 Application des migrations...")
        try:
            upgrade()
            print("✅ Migrations appliquées")
        except Exception as e:
            print(f"⚠️  Erreur lors de l'application des migrations: {e}")
            print("   Vérifiez que la base de données est accessible")
        
        print("\n✅ Initialisation terminée!")
        print("\n📝 Commandes utiles:")
        print("   Créer une migration: flask db migrate -m 'Description'")
        print("   Appliquer migrations: flask db upgrade")
        print("   Revenir en arrière: flask db downgrade")
        
        return True


if __name__ == '__main__':
    success = init_migrations()
    sys.exit(0 if success else 1)

