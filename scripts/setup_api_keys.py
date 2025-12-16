#!/usr/bin/env python3
"""
Script non-interactif pour configurer les clés API des plateformes boursières.
Usage: 
  python scripts/setup_api_keys.py --alphavantage VOTRE_CLE
  python scripts/setup_api_keys.py --iex-cloud sk-VOTRE_CLE
  python scripts/setup_api_keys.py --alphavantage VOTRE_CLE --iex-cloud sk-VOTRE_CLE
"""
import os
import sys
import re
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Encodage pour Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def validate_alphavantage_key(key):
    """Valide le format d'une clé Alpha Vantage."""
    if not key:
        return False, "Clé vide"
    if len(key) < 10:
        return False, "Clé trop courte (minimum 10 caractères)"
    if not re.match(r'^[A-Z0-9]+$', key.upper()):
        return False, "Format invalide (lettres majuscules et chiffres uniquement)"
    return True, "OK"

def validate_iex_key(key):
    """Valide le format d'une clé IEX Cloud."""
    if not key:
        return False, "Clé vide"
    if not re.match(r'^(sk|pk)-[a-zA-Z0-9]+$', key):
        return False, "Format invalide (doit commencer par 'sk-' ou 'pk-')"
    return True, "OK"

def get_env_path():
    """Retourne le chemin du fichier .env."""
    project_root = Path(__file__).parent.parent
    env_path = project_root / '.env'
    return env_path

def read_env_file():
    """Lit le fichier .env et retourne un dictionnaire."""
    env_path = get_env_path()
    if not env_path.exists():
        return {}
    
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

def write_env_file(env_vars):
    """Écrit le fichier .env."""
    env_path = get_env_path()
    
    # Lire les lignes existantes pour préserver les commentaires
    existing_lines = []
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            existing_lines = f.readlines()
    
    # Créer un nouveau contenu
    new_lines = []
    keys_written = set()
    
    # Préserver les lignes existantes (sauf celles qu'on modifie)
    for line in existing_lines:
        line_stripped = line.strip()
        if line_stripped and not line_stripped.startswith('#') and '=' in line_stripped:
            key = line_stripped.split('=', 1)[0].strip()
            if key in env_vars:
                # Remplacer par la nouvelle valeur
                new_lines.append(f"{key}={env_vars[key]}\n")
                keys_written.add(key)
            else:
                # Garder la ligne originale
                new_lines.append(line)
        else:
            # Garder les commentaires et lignes vides
            new_lines.append(line)
    
    # Ajouter les nouvelles clés
    for key, value in env_vars.items():
        if key not in keys_written:
            new_lines.append(f"{key}={value}\n")
    
    # Écrire le fichier
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def setup_alphavantage(key):
    """Configure la clé API Alpha Vantage."""
    is_valid, message = validate_alphavantage_key(key)
    if not is_valid:
        print(f"❌ Erreur de validation Alpha Vantage: {message}")
        return False
    
    env_vars = read_env_file()
    env_vars['ALPHAVANTAGE_KEY'] = key.upper()
    write_env_file(env_vars)
    
    print(f"✅ Clé Alpha Vantage configurée avec succès!")
    return True

def setup_iex_cloud(key):
    """Configure la clé API IEX Cloud."""
    is_valid, message = validate_iex_key(key)
    if not is_valid:
        print(f"❌ Erreur de validation IEX Cloud: {message}")
        return False
    
    env_vars = read_env_file()
    env_vars['IEX_CLOUD_API_KEY'] = key
    write_env_file(env_vars)
    
    print(f"✅ Clé IEX Cloud configurée avec succès!")
    return True

def show_config():
    """Affiche la configuration actuelle."""
    env_vars = read_env_file()
    
    print("\n" + "=" * 70)
    print("CONFIGURATION ACTUELLE")
    print("=" * 70)
    
    # Alpha Vantage
    alphavantage_key = env_vars.get('ALPHAVANTAGE_KEY', '')
    if alphavantage_key:
        masked = alphavantage_key[:10] + '...' + alphavantage_key[-4:] if len(alphavantage_key) > 14 else '***'
        print(f"✅ Alpha Vantage: {masked}")
    else:
        print("❌ Alpha Vantage: Non configurée")
    
    # IEX Cloud
    iex_key = env_vars.get('IEX_CLOUD_API_KEY', '')
    if iex_key:
        masked = iex_key[:5] + '...' + iex_key[-4:] if len(iex_key) > 9 else '***'
        print(f"✅ IEX Cloud: {masked}")
    else:
        print("❌ IEX Cloud: Non configurée")
    
    # Yahoo Finance
    print("✅ Yahoo Finance: Disponible (pas de clé requise)")

def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(
        description='Configure les clés API des plateformes boursières',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  # Configurer Alpha Vantage uniquement
  python scripts/setup_api_keys.py --alphavantage DEMO1234567890ABC
  
  # Configurer IEX Cloud uniquement
  python scripts/setup_api_keys.py --iex-cloud sk-1234567890abcdef
  
  # Configurer les deux
  python scripts/setup_api_keys.py --alphavantage DEMO1234567890ABC --iex-cloud sk-1234567890abcdef
  
  # Afficher la configuration actuelle
  python scripts/setup_api_keys.py --show

Pour obtenir les clés:
  - Alpha Vantage: https://www.alphavantage.co/support/#api-key
  - IEX Cloud: https://iexcloud.io/console/tokens
        """
    )
    
    parser.add_argument('--alphavantage', '-a', 
                       help='Clé API Alpha Vantage')
    parser.add_argument('--iex-cloud', '-i',
                       help='Clé API IEX Cloud (format: sk-xxx ou pk-xxx)')
    parser.add_argument('--show', '-s', 
                       action='store_true',
                       help='Afficher la configuration actuelle')
    
    args = parser.parse_args()
    
    if args.show:
        show_config()
        return 0
    
    if not args.alphavantage and not args.iex_cloud:
        parser.print_help()
        print("\n💡 Astuce: Utilisez --show pour voir la configuration actuelle")
        return 1
    
    success = True
    
    if args.alphavantage:
        if not setup_alphavantage(args.alphavantage):
            success = False
    
    if args.iex_cloud:
        if not setup_iex_cloud(args.iex_cloud):
            success = False
    
    if success:
        print("\n" + "=" * 70)
        print("✅ Configuration terminée!")
        print("=" * 70)
        print("\n💡 Note: Redémarrez l'application pour que les changements prennent effet.")
        show_config()
        return 0
    else:
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Configuration annulée")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

