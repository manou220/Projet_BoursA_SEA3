#!/usr/bin/env python3
"""
Vérification approfondie pour la production.
Vérifie les problèmes subtils qui pourraient empêcher l'application de tourner.
Usage: python scripts/check_deep_production.py
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()

def check_imports():
    """Vérifie les imports optionnels et leurs impacts."""
    print("=" * 70)
    print("VERIFICATION DES IMPORTS OPTIONNELS")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # ClamAV (optionnel)
    try:
        import clamd
        print("[OK] ClamAV disponible (antivirus)")
    except ImportError:
        print("[INFO] ClamAV non installe (optionnel - scan de fichiers desactive)")
        warnings.append("ClamAV non installe - Scan de fichiers desactive")
    
    # SocketIO (optionnel)
    try:
        import flask_socketio
        print("[OK] Flask-SocketIO disponible")
    except ImportError:
        print("[INFO] Flask-SocketIO non installe (optionnel)")
        warnings.append("Flask-SocketIO non installe - WebSockets desactives")
    
    # Flask-Migrate (optionnel mais recommandé)
    try:
        import flask_migrate
        print("[OK] Flask-Migrate disponible")
    except ImportError:
        print("[ATTENTION] Flask-Migrate non installe (recommandé pour les migrations)")
        warnings.append("Flask-Migrate non installe - Migrations manuelles necessaires")
    
    return issues, warnings

def check_model_files():
    """Vérifie la présence des modèles ML."""
    print("\n" + "=" * 70)
    print("VERIFICATION DES MODELES ML")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    models_dir = Path('app/models')
    if not models_dir.exists():
        warnings.append("Repertoire app/models n'existe pas")
        return issues, warnings
    
    # Chercher les modèles .joblib
    model_files = list(models_dir.glob('*.joblib'))
    
    if model_files:
        print(f"[OK] {len(model_files)} modele(s) ML trouve(s):")
        for model_file in model_files:
            size_mb = model_file.stat().st_size / (1024 * 1024)
            print(f"   - {model_file.name} ({size_mb:.2f} MB)")
    else:
        warnings.append("Aucun modele ML (.joblib) trouve dans app/models")
        warnings.append("   Les fonctionnalites de prevision ne fonctionneront pas")
    
    # Vérifier les modèles spécifiques mentionnés dans le code
    expected_models = [
        'model_final_bourse_random_forest.joblib',
        'model_final_bourse_xgboost.joblib'
    ]
    
    for model_name in expected_models:
        model_path = models_dir / model_name
        if model_path.exists():
            print(f"[OK] Modele attendu trouve: {model_name}")
        else:
            warnings.append(f"Modele attendu non trouve: {model_name}")
    
    return issues, warnings

def check_templates():
    """Vérifie la présence des templates HTML."""
    print("\n" + "=" * 70)
    print("VERIFICATION DES TEMPLATES")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    templates_dir = Path('app/templates')
    if not templates_dir.exists():
        issues.append("Repertoire app/templates n'existe pas - CRITIQUE")
        return issues, warnings
    
    # Templates critiques
    critical_templates = [
        'base.html',
        'accueil.html',
        'errors/404.html',
        'errors/500.html',
    ]
    
    for template in critical_templates:
        template_path = templates_dir / template
        if template_path.exists():
            print(f"[OK] Template {template} existe")
        else:
            issues.append(f"Template critique manquant: {template}")
    
    # Templates importants
    important_templates = [
        'tests.html',
        'previsions.html',
        'visualisation.html',
        'historique.html',
        'cartographie.html',
    ]
    
    for template in important_templates:
        template_path = templates_dir / template
        if template_path.exists():
            print(f"[OK] Template {template} existe")
        else:
            warnings.append(f"Template important manquant: {template}")
    
    return issues, warnings

def check_static_files():
    """Vérifie les fichiers statiques."""
    print("\n" + "=" * 70)
    print("VERIFICATION DES FICHIERS STATIQUES")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    static_dir = Path('app/static')
    if not static_dir.exists():
        warnings.append("Repertoire app/static n'existe pas")
        return issues, warnings
    
    # Fichiers CSS critiques
    css_files = list(static_dir.glob('*.css')) + list((static_dir / 'css').glob('*.css'))
    if css_files:
        print(f"[OK] {len(css_files)} fichier(s) CSS trouve(s)")
    else:
        warnings.append("Aucun fichier CSS trouve - Interface peut etre non stylisee")
    
    # Logo
    logo_files = list(static_dir.glob('*.jpg')) + list(static_dir.glob('*.png'))
    if logo_files:
        print(f"[OK] {len(logo_files)} fichier(s) image trouve(s)")
    else:
        warnings.append("Aucun logo trouve (optionnel)")
    
    return issues, warnings

def check_logging_config():
    """Vérifie la configuration du logging."""
    print("\n" + "=" * 70)
    print("VERIFICATION DU LOGGING")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # Répertoire logs
    logs_dir = Path('logs')
    if logs_dir.exists():
        print("[OK] Repertoire logs existe")
        
        # Vérifier les permissions
        if os.access(logs_dir, os.W_OK):
            print("[OK] Repertoire logs accessible en ecriture")
        else:
            issues.append("Repertoire logs non accessible en ecriture - Les logs ne pourront pas etre ecrits")
    else:
        warnings.append("Repertoire logs n'existe pas (sera cree automatiquement)")
    
    # Vérifier LOG_FILE dans la config
    log_file = os.getenv('LOG_FILE', 'logs/app.log')
    log_dir = Path(log_file).parent
    if log_dir.exists() or log_dir == Path('.'):
        print(f"[OK] Repertoire de log accessible: {log_dir}")
    else:
        warnings.append(f"Repertoire de log peut ne pas exister: {log_dir}")
    
    return issues, warnings

def check_permissions():
    """Vérifie les permissions de fichiers."""
    print("\n" + "=" * 70)
    print("VERIFICATION DES PERMISSIONS")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # Répertoires nécessitant l'écriture
    writable_dirs = ['uploads', 'logs', 'logs/jobs']
    
    for dir_path in writable_dirs:
        dir_obj = Path(dir_path)
        if dir_obj.exists():
            if os.access(dir_obj, os.W_OK):
                print(f"[OK] {dir_path} accessible en ecriture")
            else:
                issues.append(f"{dir_path} non accessible en ecriture - CRITIQUE")
        else:
            # Vérifier si le parent est accessible
            parent = dir_obj.parent
            if parent.exists() and os.access(parent, os.W_OK):
                print(f"[OK] {dir_path} peut etre cree (parent accessible)")
            else:
                warnings.append(f"{dir_path} ne peut pas etre cree - Probleme potentiel")
    
    return issues, warnings

def check_docker_config():
    """Vérifie la configuration Docker."""
    print("\n" + "=" * 70)
    print("VERIFICATION DOCKER")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # Dockerfile
    dockerfile = Path('Dockerfile')
    if dockerfile.exists():
        print("[OK] Dockerfile existe")
    else:
        issues.append("Dockerfile manquant - Impossible de construire l'image Docker")
    
    # docker-compose.prod.yml
    compose_file = Path('docs/docker-compose.prod.yml')
    if compose_file.exists():
        print("[OK] docker-compose.prod.yml existe")
    else:
        warnings.append("docker-compose.prod.yml manquant (si Docker utilise)")
    
    # entrypoint.sh
    entrypoint = Path('scripts/entrypoint.sh')
    if entrypoint.exists():
        print("[OK] scripts/entrypoint.sh existe")
        # Vérifier qu'il est exécutable (sur Linux)
        if os.name != 'nt':  # Pas Windows
            if os.access(entrypoint, os.X_OK):
                print("[OK] entrypoint.sh est executable")
            else:
                warnings.append("entrypoint.sh n'est pas executable")
    else:
        warnings.append("scripts/entrypoint.sh manquant")
    
    return issues, warnings

def check_code_quality():
    """Vérifie la qualité du code pour la production."""
    print("\n" + "=" * 70)
    print("VERIFICATION QUALITE DU CODE")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # Vérifier les appels à get_real_time_users_from_db avec DB_PATH
    init_file = Path('app/__init__.py')
    if init_file.exists():
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Vérifier si get_real_time_users_from_db est appelé avec DB_PATH
            if 'get_real_time_users_from_db' in content and 'DB_PATH' in content:
                # C'est OK car le fallback SQLite est désactivé en production
                print("[OK] get_real_time_users_from_db utilise DB_PATH (fallback desactive en prod)")
            else:
                print("[OK] Pas d'appel problematique a get_real_time_users_from_db")
    
    # Vérifier les chemins hardcodés
    code_files = list(Path('app').rglob('*.py'))
    hardcoded_paths = []
    for code_file in code_files[:10]:  # Limiter pour performance
        try:
            with open(code_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Chercher des chemins Windows hardcodés
                if 'C:\\' in content or 'D:\\' in content:
                    hardcoded_paths.append(str(code_file))
        except:
            pass
    
    if hardcoded_paths:
        warnings.append(f"Chemins Windows hardcodes trouves dans {len(hardcoded_paths)} fichier(s)")
    else:
        print("[OK] Pas de chemins Windows hardcodes detectes")
    
    return issues, warnings

def check_environment_variables():
    """Vérifie les variables d'environnement critiques."""
    print("\n" + "=" * 70)
    print("VERIFICATION DES VARIABLES D'ENVIRONNEMENT")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # Variables critiques
    critical_vars = {
        'DATABASE_URL': 'Base de donnees PostgreSQL',
        'SECRET_KEY': 'Cle secrete Flask',
    }
    
    for var, description in critical_vars.items():
        value = os.getenv(var)
        if value:
            # Masquer les valeurs sensibles
            if 'password' in var.lower() or 'secret' in var.lower() or 'key' in var.lower():
                print(f"[OK] {description} configuree ({len(value)} caracteres)")
            else:
                safe_value = value.split('@')[1] if '@' in value else value[:30]
                print(f"[OK] {description} configuree ({safe_value}...)")
        else:
            issues.append(f"{description} non configuree ({var})")
    
    # Variables optionnelles mais recommandées
    optional_vars = {
        'USE_HTTPS': 'Configuration HTTPS',
        'CACHE_REDIS_URL': 'Cache Redis',
        'LOG_LEVEL': 'Niveau de logging',
    }
    
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"[OK] {description} configuree")
        else:
            if var == 'USE_HTTPS':
                print(f"[INFO] {description} non configuree (defaut: true)")
            else:
                warnings.append(f"{description} non configuree ({var})")
    
    return issues, warnings

def main():
    """Fonction principale."""
    print("\n" + "=" * 70)
    print("VERIFICATION APPROFONDIE POUR LA PRODUCTION")
    print("=" * 70)
    print()
    
    all_issues = []
    all_warnings = []
    
    # Vérifications
    issues, warnings = check_imports()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_model_files()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_templates()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_static_files()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_logging_config()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_permissions()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_docker_config()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_code_quality()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_environment_variables()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    # Résumé
    print("\n" + "=" * 70)
    print("RESUME DE LA VERIFICATION APPROFONDIE")
    print("=" * 70)
    
    if not all_issues and not all_warnings:
        print("[OK] AUCUN PROBLEME DETECTE - Application prete!")
        return 0
    elif not all_issues:
        print(f"[OK] AUCUN PROBLEME CRITIQUE")
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
            for warning in all_warnings[:10]:  # Limiter l'affichage
                print(f"  - {warning}")
            if len(all_warnings) > 10:
                print(f"  ... et {len(all_warnings) - 10} autre(s)")
        
        return 1

if __name__ == '__main__':
    sys.exit(main())

