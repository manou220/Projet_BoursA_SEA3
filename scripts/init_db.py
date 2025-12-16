#!/usr/bin/env python3
"""
Script d'initialisation de la base de données.
Crée toutes les tables nécessaires et initialise les données de base.
Usage: python scripts/init_db.py
"""
import os
import sys

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.user import User, Role, init_users_table
from app.models.data_file import DataFile
from app.models.test_history import TestHistory
from app.models.user_location import UserLocation


def init_database():
    """Initialise la base de données avec toutes les tables."""
    app = create_app()
    
    with app.app_context():
        print("[INFO] Initialisation de la base de donnees...")
        
        # Créer toutes les tables
        print("[INFO] Creation des tables...")
        try:
            db.create_all()
            print("[OK] Tables creees avec succes")
        except Exception as e:
            print(f"[ERREUR] Erreur lors de la creation des tables: {e}")
            return False
        
        # Initialiser la table des utilisateurs
        print("[INFO] Initialisation de la table utilisateurs...")
        try:
            init_users_table()
            print("[OK] Table utilisateurs initialisee")
        except Exception as e:
            print(f"[ATTENTION] Erreur lors de l'initialisation des utilisateurs: {e}")
            # Ne pas échouer si l'admin existe déjà
        
        # Seed des localisations si nécessaire
        print("[INFO] Verification des localisations...")
        try:
            from app.utils import _seed_sample_locations_sqlalchemy
            locations = UserLocation.get_all_locations()
            if len(locations) == 0:
                print("[INFO] Ajout de donnees d'exemple pour les localisations...")
                _seed_sample_locations_sqlalchemy()
                print("[OK] Donnees d'exemple ajoutees")
            else:
                print(f"[OK] {len(locations)} localisations trouvees")
        except Exception as e:
            print(f"[ATTENTION] Erreur lors de l'initialisation des localisations: {e}")
        
        # Vérifier que les tables existent
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['users', 'data_files', 'test_history', 'user_locations']
        missing_tables = [t for t in expected_tables if t not in tables]
        
        if missing_tables:
            print(f"[ATTENTION] Tables manquantes: {missing_tables}")
        else:
            print("[OK] Toutes les tables sont presentes")
        
        # Afficher le résumé
        print("\n[RESUME]:")
        for table in expected_tables:
            if table in tables:
                try:
                    count = db.session.execute(db.text(f"SELECT COUNT(*) FROM {table}")).scalar()
                    print(f"  - {table}: {count} lignes")
                except Exception as e:
                    print(f"  - {table}: erreur lors du comptage ({e})")
        
        print("\n[OK] Initialisation terminee avec succes!")
        return True


if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
