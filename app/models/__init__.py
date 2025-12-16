"""
Modèles de données de l'application.
"""

# Importer tous les modèles pour qu'ils soient enregistrés avec SQLAlchemy
from app.models.user import User, Role, Permission
from app.models.data_file import DataFile
from app.models.test_history import TestHistory
from app.models.user_location import UserLocation

__all__ = [
    'User',
    'Role',
    'Permission',
    'DataFile',
    'TestHistory',
    'UserLocation',
]

