#!/usr/bin/env python3
"""
Script de test pour valider les corrections apportées au projet.
"""

import os
import sys
import pytest
import joblib

CONFIG_FILES = [
    ('wsgi.py', 'wsgi.py'),
    ('app/__init__.py', 'app/__init__.py'),
    ('app/config.py', 'app/config.py'),
    ('app/extensions.py', 'app/extensions.py'),
    ('Dockerfile', 'Dockerfile'),
    ('Docker-compose.yml', 'Docker-compose.yml'),
]

DIRECTORIES = [
    ('uploads', 'Dossier uploads'),
    ('app/models', 'Dossier app/models'),
    ('app/templates', 'Dossier app/templates'),
    ('app/static', 'Dossier app/static'),
]


@pytest.mark.parametrize("filepath,description", CONFIG_FILES)
def test_file_exists(filepath, description):
    """Teste si un fichier existe."""
    assert os.path.exists(filepath), f"Fichier manquant: {description}"


@pytest.mark.parametrize("filepath,description", CONFIG_FILES)
def test_file_not_empty(filepath, description):
    """Teste si un fichier n'est pas vide."""
    assert os.path.exists(filepath), f"Fichier inexistant: {description}"
    size = os.path.getsize(filepath)
    assert size > 0, f"Fichier vide: {description}"


@pytest.mark.parametrize("dirpath,description", DIRECTORIES)
def test_directory_exists(dirpath, description):
    """Teste si un dossier existe."""
    assert os.path.isdir(dirpath), f"Dossier manquant: {description}"


def test_no_model1_reference():
    """Teste qu'il n'y a plus de référence à Model1 dans app.py."""
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'Model1' not in content, "Référence à 'Model1' trouvée dans app.py"
    

def test_models_accessible():
    """Teste que les modèles ML sont accessibles."""
    models_dir = os.path.join('app', 'models')
    joblib_files = [f for f in os.listdir(models_dir) if f.endswith('.joblib')]
    
    # Si aucun modèle, considérer comme échec explicite
    assert joblib_files, "Aucun modèle .joblib trouvé dans app/models"

    for file in joblib_files:
        filepath = os.path.join(models_dir, file)
        joblib.load(filepath)  # doit charger sans erreur


if __name__ == '__main__':
    # Permet d'exécuter ce fichier comme script autonome si besoin
    sys.exit(pytest.main([__file__]))
