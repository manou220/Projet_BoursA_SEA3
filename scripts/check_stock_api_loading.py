#!/usr/bin/env python3
"""
Vérification du chargement de fichiers via les plateformes boursières.
Usage: python scripts/check_stock_api_loading.py
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()

def check_dependencies():
    """Vérifie les dépendances nécessaires."""
    print("=" * 70)
    print("VERIFICATION DES DEPENDANCES")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # yfinance
    try:
        import yfinance as yf
        print("[OK] yfinance installe")
    except ImportError:
        issues.append("yfinance non installe - Necessaire pour Yahoo Finance")
        print("[ERREUR] yfinance non installe")
    
    # requests
    try:
        import requests
        print("[OK] requests installe")
    except ImportError:
        issues.append("requests non installe - Necessaire pour les APIs")
        print("[ERREUR] requests non installe")
    
    # pandas
    try:
        import pandas as pd
        print("[OK] pandas installe")
    except ImportError:
        issues.append("pandas non installe - Necessaire pour les donnees")
        print("[ERREUR] pandas non installe")
    
    return issues, warnings

def check_service_file():
    """Vérifie que le service API boursière existe."""
    print("\n" + "=" * 70)
    print("VERIFICATION DU SERVICE API BOURSIERE")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    service_file = Path('app/services/stock_api_service.py')
    if service_file.exists():
        print("[OK] Service API boursiere present (app/services/stock_api_service.py)")
    else:
        issues.append("Service API boursiere manquant")
        return issues, warnings
    
    # Vérifier les imports dans le service
    try:
        with open(service_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Vérifier les imports critiques
            if 'import yfinance' in content or 'import yfinance as yf' in content:
                print("[OK] Import yfinance present")
            else:
                warnings.append("Import yfinance manquant dans le service")
            
            if 'import requests' in content:
                print("[OK] Import requests present")
            else:
                warnings.append("Import requests manquant dans le service")
            
            if 'import pandas' in content or 'import pandas as pd' in content:
                print("[OK] Import pandas present")
            else:
                warnings.append("Import pandas manquant dans le service")
            
            # Vérifier les méthodes critiques
            if 'def fetch_stock_data' in content:
                print("[OK] Methode fetch_stock_data presente")
            else:
                issues.append("Methode fetch_stock_data manquante")
            
            if 'def _fetch_yahoo' in content:
                print("[OK] Methode _fetch_yahoo presente")
            else:
                warnings.append("Methode _fetch_yahoo manquante")
            
            if 'def _fetch_alpha_vantage' in content:
                print("[OK] Methode _fetch_alpha_vantage presente")
            else:
                warnings.append("Methode _fetch_alpha_vantage manquante")
            
            if 'def _fetch_iex_cloud' in content:
                print("[OK] Methode _fetch_iex_cloud presente")
            else:
                warnings.append("Methode _fetch_iex_cloud manquante")
            
            # Vérifier la gestion d'erreurs
            if 'class StockAPIError' in content:
                print("[OK] Classe StockAPIError presente")
            else:
                warnings.append("Classe StockAPIError manquante")
            
            if 'class RateLimitExceeded' in content:
                print("[OK] Classe RateLimitExceeded presente")
            else:
                warnings.append("Classe RateLimitExceeded manquante")
            
    except Exception as e:
        issues.append(f"Erreur lors de la lecture du service: {e}")
    
    return issues, warnings

def check_upload_route():
    """Vérifie la route d'upload API."""
    print("\n" + "=" * 70)
    print("VERIFICATION DE LA ROUTE D'UPLOAD API")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    upload_file = Path('app/blueprints/upload/routes.py')
    if not upload_file.exists():
        issues.append("Fichier routes.py manquant")
        return issues, warnings
    
    try:
        with open(upload_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Vérifier la route api_fetch
            if '@bp.route(\'/upload/api_fetch' in content or "@bp.route('/upload/api_fetch" in content:
                print("[OK] Route /upload/api_fetch presente")
            else:
                issues.append("Route /upload/api_fetch manquante")
            
            # Vérifier l'utilisation du service
            if 'get_stock_api_service' in content:
                print("[OK] Utilisation de get_stock_api_service")
            else:
                issues.append("get_stock_api_service non utilise")
            
            # Vérifier la gestion d'erreurs
            if 'RateLimitExceeded' in content:
                print("[OK] Gestion de RateLimitExceeded presente")
            else:
                warnings.append("Gestion de RateLimitExceeded manquante")
            
            if 'StockAPIError' in content:
                print("[OK] Gestion de StockAPIError presente")
            else:
                warnings.append("Gestion de StockAPIError manquante")
            
            # Vérifier la sauvegarde de fichier
            if 'secure_filename' in content:
                print("[OK] Utilisation de secure_filename pour la securite")
            else:
                warnings.append("secure_filename non utilise")
            
    except Exception as e:
        issues.append(f"Erreur lors de la lecture de routes.py: {e}")
    
    return issues, warnings

def check_api_keys():
    """Vérifie la configuration des clés API."""
    print("\n" + "=" * 70)
    print("VERIFICATION DES CLES API")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # Yahoo Finance - pas de clé requise
    print("[OK] Yahoo Finance: Pas de cle API requise (toujours disponible)")
    
    # Alpha Vantage
    alphavantage_key = os.getenv('ALPHAVANTAGE_KEY')
    if alphavantage_key:
        print(f"[OK] Alpha Vantage: Cle API configuree ({len(alphavantage_key)} caracteres)")
    else:
        warnings.append("Alpha Vantage: Cle API non configuree (ALPHAVANTAGE_KEY)")
        print("[ATTENTION] Alpha Vantage: Cle API non configuree")
    
    # IEX Cloud
    iex_key = os.getenv('IEX_CLOUD_API_KEY')
    if iex_key:
        print(f"[OK] IEX Cloud: Cle API configuree ({len(iex_key)} caracteres)")
    else:
        warnings.append("IEX Cloud: Cle API non configuree (IEX_CLOUD_API_KEY)")
        print("[ATTENTION] IEX Cloud: Cle API non configuree")
    
    return issues, warnings

def check_cache_config():
    """Vérifie la configuration du cache."""
    print("\n" + "=" * 70)
    print("VERIFICATION DU CACHE")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    cache_url = os.getenv('CACHE_REDIS_URL')
    if cache_url:
        print(f"[OK] Cache Redis configure: {cache_url.split('@')[1] if '@' in cache_url else 'configure'}")
    else:
        print("[INFO] Cache Redis non configure - SimpleCache utilise (en memoire)")
        warnings.append("Cache Redis non configure - Performance reduite avec plusieurs instances")
    
    return issues, warnings

def check_upload_folder():
    """Vérifie le répertoire d'upload."""
    print("\n" + "=" * 70)
    print("VERIFICATION DU REPERTOIRE D'UPLOAD")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    upload_folder = Path('uploads')
    if upload_folder.exists():
        print("[OK] Repertoire uploads existe")
        
        # Vérifier les permissions
        if os.access(upload_folder, os.W_OK):
            print("[OK] Repertoire uploads accessible en ecriture")
        else:
            issues.append("Repertoire uploads non accessible en ecriture")
    else:
        warnings.append("Repertoire uploads n'existe pas (sera cree automatiquement)")
    
    return issues, warnings

def test_yahoo_connection():
    """Teste une connexion simple à Yahoo Finance."""
    print("\n" + "=" * 70)
    print("TEST DE CONNEXION YAHOO FINANCE")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    try:
        import yfinance as yf
        
        # Test simple avec un symbole connu
        print("Test de connexion avec AAPL...")
        ticker = yf.Ticker("AAPL")
        info = ticker.info
        
        if info and 'symbol' in info:
            print(f"[OK] Connexion Yahoo Finance reussie (symbole: {info.get('symbol', 'N/A')})")
        else:
            warnings.append("Connexion Yahoo Finance reussie mais donnees invalides")
            
    except ImportError:
        issues.append("yfinance non installe - Impossible de tester")
    except Exception as e:
        warnings.append(f"Erreur lors du test Yahoo Finance: {str(e)}")
        print(f"[ATTENTION] Erreur de connexion: {str(e)}")
    
    return issues, warnings

def check_rate_limiting():
    """Vérifie la configuration du rate limiting."""
    print("\n" + "=" * 70)
    print("VERIFICATION DU RATE LIMITING")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    service_file = Path('app/services/stock_api_service.py')
    if service_file.exists():
        try:
            with open(service_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Vérifier les quotas
                if 'API_QUOTAS' in content:
                    print("[OK] Configuration des quotas API presente")
                else:
                    warnings.append("Configuration des quotas API manquante")
                
                # Vérifier le rate limiting
                if '_check_rate_limit' in content:
                    print("[OK] Methode de rate limiting presente")
                else:
                    warnings.append("Methode de rate limiting manquante")
                
        except Exception as e:
            warnings.append(f"Erreur lors de la verification: {e}")
    
    return issues, warnings

def main():
    """Fonction principale."""
    print("\n" + "=" * 70)
    print("VERIFICATION DU CHARGEMENT DE FICHIERS VIA PLATEFORMES BOURSIERES")
    print("=" * 70)
    print()
    
    all_issues = []
    all_warnings = []
    
    # Vérifications
    issues, warnings = check_dependencies()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_service_file()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_upload_route()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_api_keys()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_cache_config()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_upload_folder()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_rate_limiting()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = test_yahoo_connection()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    # Résumé
    print("\n" + "=" * 70)
    print("RESUME DE LA VERIFICATION")
    print("=" * 70)
    
    if not all_issues and not all_warnings:
        print("[OK] AUCUN PROBLEME DETECTE - Chargement de fichiers boursiers OK!")
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
            for warning in all_warnings[:10]:
                print(f"  - {warning}")
            if len(all_warnings) > 10:
                print(f"  ... et {len(all_warnings) - 10} autre(s)")
        
        return 1

if __name__ == '__main__':
    sys.exit(main())

