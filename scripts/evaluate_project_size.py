#!/usr/bin/env python3
"""
Évaluation de la taille du projet.
Analyse les fichiers, lignes de code, dépendances, etc.
Usage: python scripts/evaluate_project_size.py
"""
import os
import sys
from pathlib import Path
from collections import defaultdict
import json

# Encodage pour Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def print_header(text):
    """Affiche un en-tête formaté."""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)

def get_file_size(file_path):
    """Retourne la taille d'un fichier en octets."""
    try:
        return file_path.stat().st_size
    except:
        return 0

def count_lines(file_path):
    """Compte les lignes d'un fichier."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return len(f.readlines())
    except:
        return 0

def format_size(size_bytes):
    """Formate une taille en octets en format lisible."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def analyze_project():
    """Analyse la taille du projet."""
    project_root = Path(__file__).parent.parent
    
    # Statistiques globales
    stats = {
        'total_files': 0,
        'total_lines': 0,
        'total_size': 0,
        'by_extension': defaultdict(lambda: {'count': 0, 'lines': 0, 'size': 0}),
        'by_directory': defaultdict(lambda: {'count': 0, 'lines': 0, 'size': 0}),
        'python_files': [],
        'largest_files': [],
        'directories': []
    }
    
    # Extensions à ignorer
    ignore_extensions = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe', '.db', '.sqlite', '.log'}
    ignore_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'env', '.env', 'dist', 'build', '.pytest_cache', '.mypy_cache'}
    
    # Parcourir tous les fichiers
    for root, dirs, files in os.walk(project_root):
        # Filtrer les répertoires à ignorer
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        root_path = Path(root)
        rel_path = root_path.relative_to(project_root)
        
        for file in files:
            file_path = root_path / file
            
            # Ignorer les fichiers cachés et certains types
            if file.startswith('.') and file != '.env':
                continue
            
            # Obtenir l'extension
            ext = file_path.suffix.lower()
            if ext in ignore_extensions:
                continue
            
            # Statistiques
            size = get_file_size(file_path)
            lines = count_lines(file_path) if ext in {'.py', '.js', '.html', '.css', '.md', '.txt', '.yml', '.yaml', '.json', '.sh', '.bat', '.ps1'} else 0
            
            stats['total_files'] += 1
            stats['total_lines'] += lines
            stats['total_size'] += size
            
            # Par extension
            ext_key = ext if ext else '(sans extension)'
            stats['by_extension'][ext_key]['count'] += 1
            stats['by_extension'][ext_key]['lines'] += lines
            stats['by_extension'][ext_key]['size'] += size
            
            # Par répertoire
            dir_key = str(rel_path) if rel_path != Path('.') else 'racine'
            stats['by_directory'][dir_key]['count'] += 1
            stats['by_directory'][dir_key]['lines'] += lines
            stats['by_directory'][dir_key]['size'] += size
            
            # Fichiers Python
            if ext == '.py':
                stats['python_files'].append({
                    'path': str(rel_path / file),
                    'lines': lines,
                    'size': size
                })
            
            # Plus gros fichiers
            stats['largest_files'].append({
                'path': str(rel_path / file),
                'size': size,
                'lines': lines
            })
    
    # Trier les plus gros fichiers
    stats['largest_files'].sort(key=lambda x: x['size'], reverse=True)
    stats['largest_files'] = stats['largest_files'][:20]
    
    # Trier les fichiers Python par taille
    stats['python_files'].sort(key=lambda x: x['lines'], reverse=True)
    
    return stats

def analyze_dependencies():
    """Analyse les dépendances du projet."""
    project_root = Path(__file__).parent.parent
    
    dependencies = {
        'python': [],
        'node': [],
        'system': []
    }
    
    # requirements.txt
    req_file = project_root / 'requirements.txt'
    if req_file.exists():
        try:
            with open(req_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '==' in line:
                            pkg, version = line.split('==', 1)
                            dependencies['python'].append({'name': pkg.strip(), 'version': version.strip()})
                        elif '>=' in line:
                            pkg, version = line.split('>=', 1)
                            dependencies['python'].append({'name': pkg.strip(), 'version': f">={version.strip()}"})
                        else:
                            dependencies['python'].append({'name': line, 'version': 'non spécifié'})
        except Exception as e:
            print(f"⚠️  Erreur lecture requirements.txt: {e}")
    
    # package.json
    pkg_file = project_root / 'package.json'
    if pkg_file.exists():
        try:
            with open(pkg_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'dependencies' in data:
                    for pkg, version in data['dependencies'].items():
                        dependencies['node'].append({'name': pkg, 'version': version})
        except:
            pass
    
    return dependencies

def analyze_structure():
    """Analyse la structure du projet."""
    project_root = Path(__file__).parent.parent
    
    structure = {
        'main_directories': [],
        'config_files': [],
        'documentation_files': [],
        'test_files': []
    }
    
    # Répertoires principaux
    for item in project_root.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            structure['main_directories'].append(item.name)
    
    # Fichiers de configuration
    config_patterns = ['*.yml', '*.yaml', '*.json', '*.toml', '*.ini', '*.cfg', '*.conf', 'Dockerfile', 'docker-compose*.yml', '.env*', 'requirements*.txt', 'package*.json']
    for pattern in config_patterns:
        for file in project_root.rglob(pattern):
            if file.is_file() and '.git' not in str(file):
                structure['config_files'].append(str(file.relative_to(project_root)))
    
    # Documentation
    for file in project_root.rglob('*.md'):
        if file.is_file() and '.git' not in str(file):
            structure['documentation_files'].append(str(file.relative_to(project_root)))
    
    # Tests
    for file in project_root.rglob('*test*.py'):
        if file.is_file() and '.git' not in str(file):
            structure['test_files'].append(str(file.relative_to(project_root)))
    
    return structure

def main():
    """Fonction principale."""
    print("\n" + "=" * 70)
    print("EVALUATION DE LA TAILLE DU PROJET")
    print("=" * 70)
    
    # Analyse
    print("\n📊 Analyse en cours...")
    stats = analyze_project()
    dependencies = analyze_dependencies()
    structure = analyze_structure()
    
    # Résultats globaux
    print_header("RESULTATS GLOBAUX")
    print(f"Total de fichiers: {stats['total_files']:,}")
    print(f"Total de lignes de code: {stats['total_lines']:,}")
    print(f"Taille totale: {format_size(stats['total_size'])}")
    print(f"Fichiers Python: {len(stats['python_files'])}")
    
    # Par extension
    print_header("REPARTITION PAR EXTENSION")
    sorted_ext = sorted(stats['by_extension'].items(), key=lambda x: x[1]['size'], reverse=True)
    for ext, data in sorted_ext[:15]:
        print(f"{ext:20} {data['count']:4} fichiers | {data['lines']:6,} lignes | {format_size(data['size']):>10}")
    
    # Fichiers Python
    print_header("FICHIERS PYTHON (TOP 15)")
    for i, file_info in enumerate(stats['python_files'][:15], 1):
        print(f"{i:2}. {file_info['path']:50} {file_info['lines']:5,} lignes | {format_size(file_info['size']):>10}")
    
    # Plus gros fichiers
    print_header("PLUS GROS FICHIERS (TOP 15)")
    for i, file_info in enumerate(stats['largest_files'][:15], 1):
        print(f"{i:2}. {file_info['path']:50} {format_size(file_info['size']):>10} | {file_info['lines']:6,} lignes")
    
    # Répertoires
    print_header("REPARTITION PAR REPERTOIRE")
    sorted_dirs = sorted(stats['by_directory'].items(), key=lambda x: x[1]['size'], reverse=True)
    for dir_name, data in sorted_dirs[:15]:
        print(f"{dir_name:40} {data['count']:3} fichiers | {data['lines']:6,} lignes | {format_size(data['size']):>10}")
    
    # Dépendances
    print_header("DEPENDANCES")
    print(f"Python: {len(dependencies['python'])} packages")
    if dependencies['python']:
        print("\nTop 10 packages Python:")
        for i, pkg in enumerate(dependencies['python'][:10], 1):
            print(f"  {i:2}. {pkg['name']:30} {pkg['version']}")
    
    if dependencies['node']:
        print(f"\nNode.js: {len(dependencies['node'])} packages")
    
    # Structure
    print_header("STRUCTURE DU PROJET")
    print(f"Répertoires principaux: {len(structure['main_directories'])}")
    for dir_name in sorted(structure['main_directories']):
        print(f"  - {dir_name}")
    
    print(f"\nFichiers de configuration: {len(structure['config_files'])}")
    for config_file in sorted(structure['config_files'])[:10]:
        print(f"  - {config_file}")
    if len(structure['config_files']) > 10:
        print(f"  ... et {len(structure['config_files']) - 10} autres")
    
    print(f"\nFichiers de documentation: {len(structure['documentation_files'])}")
    for doc_file in sorted(structure['documentation_files'])[:10]:
        print(f"  - {doc_file}")
    if len(structure['documentation_files']) > 10:
        print(f"  ... et {len(structure['documentation_files']) - 10} autres")
    
    print(f"\nFichiers de test: {len(structure['test_files'])}")
    for test_file in sorted(structure['test_files'])[:10]:
        print(f"  - {test_file}")
    if len(structure['test_files']) > 10:
        print(f"  ... et {len(structure['test_files']) - 10} autres")
    
    # Résumé
    print_header("RESUME")
    print(f"📁 Fichiers totaux: {stats['total_files']:,}")
    print(f"📝 Lignes de code: {stats['total_lines']:,}")
    print(f"💾 Taille totale: {format_size(stats['total_size'])}")
    print(f"🐍 Fichiers Python: {len(stats['python_files'])}")
    print(f"📦 Dépendances Python: {len(dependencies['python'])}")
    print(f"📚 Documentation: {len(structure['documentation_files'])} fichiers")
    print(f"🧪 Tests: {len(structure['test_files'])} fichiers")
    
    # Estimation de complexité
    avg_lines_per_file = stats['total_lines'] / stats['total_files'] if stats['total_files'] > 0 else 0
    total_python_lines = sum(f['lines'] for f in stats['python_files'])
    
    print(f"\n📊 Métriques:")
    print(f"  - Lignes moyennes par fichier: {avg_lines_per_file:.1f}")
    print(f"  - Lignes de code Python: {total_python_lines:,}")
    print(f"  - Taille moyenne fichier: {format_size(stats['total_size'] / stats['total_files'] if stats['total_files'] > 0 else 0)}")
    
    # Classification
    print_header("CLASSIFICATION DU PROJET")
    if stats['total_lines'] < 10000:
        size_class = "Petit"
    elif stats['total_lines'] < 50000:
        size_class = "Moyen"
    elif stats['total_lines'] < 100000:
        size_class = "Grand"
    else:
        size_class = "Très grand"
    
    print(f"Taille: {size_class} ({stats['total_lines']:,} lignes)")
    print(f"Complexité: {'Faible' if len(stats['python_files']) < 50 else 'Moyenne' if len(stats['python_files']) < 150 else 'Élevée'} ({len(stats['python_files'])} fichiers Python)")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Analyse annulée")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

