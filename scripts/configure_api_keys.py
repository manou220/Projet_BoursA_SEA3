#!/usr/bin/env python3
"""
Script pour configurer les clés API des plateformes boursières.
Usage: python scripts/configure_api_keys.py
"""
import os
import sys
import re
from pathlib import Path
from dotenv import load_dotenv, set_key

# Encodage pour Windows
if sys.platform == 'win32':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

def print_header(text):
    """Affiche un en-tête formaté."""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)

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

def configure_alphavantage():
    """Configure la clé API Alpha Vantage."""
    print_header("CONFIGURATION ALPHA VANTAGE")
    
    print("\n📋 Informations Alpha Vantage:")
    print("   - Gratuit avec clé API")
    print("   - Quotas: 5 requêtes/min, 500 requêtes/jour")
    print("   - Obtenir une clé: https://www.alphavantage.co/support/#api-key")
    print()
    
    env_vars = read_env_file()
    current_key = env_vars.get('ALPHAVANTAGE_KEY', '')
    
    if current_key:
        print(f"✅ Clé actuelle configurée: {current_key[:10]}...{current_key[-4:]}")
        response = input("\nVoulez-vous la modifier? (o/n): ").strip().lower()
        if response != 'o':
            return False
    else:
        print("⚠️  Aucune clé configurée")
    
    print("\nEntrez votre clé API Alpha Vantage:")
    print("(Appuyez sur Entrée pour ignorer)")
    new_key = input("Clé API: ").strip()
    
    if not new_key:
        print("❌ Configuration annulée")
        return False
    
    # Valider la clé
    is_valid, message = validate_alphavantage_key(new_key)
    if not is_valid:
        print(f"❌ Erreur de validation: {message}")
        return False
    
    # Sauvegarder
    env_vars['ALPHAVANTAGE_KEY'] = new_key.upper()
    write_env_file(env_vars)
    
    print(f"✅ Clé Alpha Vantage configurée avec succès!")
    return True

def configure_iex_cloud():
    """Configure la clé API IEX Cloud."""
    print_header("CONFIGURATION IEX CLOUD")
    
    print("\n📋 Informations IEX Cloud:")
    print("   - Gratuit avec clé API (plan gratuit disponible)")
    print("   - Quotas: ~100 requêtes/min, ~50 000 requêtes/mois")
    print("   - Obtenir une clé: https://iexcloud.io/console/login")
    print()
    
    env_vars = read_env_file()
    current_key = env_vars.get('IEX_CLOUD_API_KEY', '')
    
    if current_key:
        # Masquer la clé
        masked = current_key[:5] + '...' + current_key[-4:] if len(current_key) > 9 else '***'
        print(f"✅ Clé actuelle configurée: {masked}")
        response = input("\nVoulez-vous la modifier? (o/n): ").strip().lower()
        if response != 'o':
            return False
    else:
        print("⚠️  Aucune clé configurée")
    
    print("\nEntrez votre clé API IEX Cloud:")
    print("(Format: sk-xxxxx ou pk-xxxxx)")
    print("(Appuyez sur Entrée pour ignorer)")
    new_key = input("Clé API: ").strip()
    
    if not new_key:
        print("❌ Configuration annulée")
        return False
    
    # Valider la clé
    is_valid, message = validate_iex_key(new_key)
    if not is_valid:
        print(f"❌ Erreur de validation: {message}")
        return False
    
    # Sauvegarder
    env_vars['IEX_CLOUD_API_KEY'] = new_key
    write_env_file(env_vars)
    
    print(f"✅ Clé IEX Cloud configurée avec succès!")
    return True

def show_current_config():
    """Affiche la configuration actuelle."""
    print_header("CONFIGURATION ACTUELLE")
    
    env_vars = read_env_file()
    
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
    
    # Yahoo Finance (toujours disponible)
    print("✅ Yahoo Finance: Disponible (pas de clé requise)")

def main():
    """Fonction principale."""
    print("\n" + "=" * 70)
    print("CONFIGURATION DES CLES API BOURSIERES")
    print("=" * 70)
    
    # Afficher la configuration actuelle
    show_current_config()
    
    print("\n" + "=" * 70)
    print("MENU")
    print("=" * 70)
    print("1. Configurer Alpha Vantage")
    print("2. Configurer IEX Cloud")
    print("3. Configurer les deux")
    print("4. Afficher la configuration actuelle")
    print("5. Quitter")
    print()
    
    choice = input("Votre choix (1-5): ").strip()
    
    if choice == '1':
        configure_alphavantage()
    elif choice == '2':
        configure_iex_cloud()
    elif choice == '3':
        configure_alphavantage()
        print()
        configure_iex_cloud()
    elif choice == '4':
        show_current_config()
    elif choice == '5':
        print("Au revoir!")
        return 0
    else:
        print("❌ Choix invalide")
        return 1
    
    # Afficher la configuration finale
    print()
    show_current_config()
    
    print("\n" + "=" * 70)
    print("✅ Configuration terminée!")
    print("=" * 70)
    print("\n💡 Note: Redémarrez l'application pour que les changements prennent effet.")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Configuration annulée par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)

