#!/usr/bin/env python3
"""
Vérification des statistiques implémentées dans l'application.
Usage: python scripts/check_statistics.py
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

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

def check_statistical_tests():
    """Vérifie les tests statistiques implémentés."""
    print_header("VERIFICATION DES TESTS STATISTIQUES")
    
    tests_found = []
    tests_missing = []
    
    # Tests dans Flask (app/blueprints/tests/routes.py)
    flask_tests_file = Path('app/blueprints/tests/routes.py')
    if flask_tests_file.exists():
        with open(flask_tests_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Tests détectés
            flask_tests = {
                'wilcoxon': 'Test de Wilcoxon',
                'mannwhitney': 'Test de Mann-Whitney U',
                'kruskal': 'Test de Kruskal-Wallis',
                'spearman': 'Corrélation de Spearman',
                'friedman': 'Test de Friedman',
                'kolmogorov_smirnov': 'Test de normalité Kolmogorov-Smirnov',
                'shapiro_wilk': 'Test de normalité Shapiro-Wilk'
            }
            
            for test_key, test_name in flask_tests.items():
                if test_key in content:
                    tests_found.append(f"Flask: {test_name}")
                    print(f"[OK] {test_name} (Flask)")
                else:
                    tests_missing.append(f"Flask: {test_name}")
    
    # Tests dans Streamlit (pages/page_tests.py)
    streamlit_tests_file = Path('pages/page_tests.py')
    if streamlit_tests_file.exists():
        with open(streamlit_tests_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            streamlit_tests = {
                'Shapiro-Wilk': 'Test de normalité Shapiro-Wilk',
                'Kolmogorov-Smirnov': 'Test de normalité Kolmogorov-Smirnov',
                'Test t de Student': 'Test t de Student',
                'Pearson': 'Corrélation de Pearson',
                'Spearman': 'Corrélation de Spearman',
                'Chi-2': 'Test du Chi-2',
                'ANOVA': 'ANOVA (analyse de variance)',
                'Mann-Whitney': 'Test de Mann-Whitney U'
            }
            
            for test_key, test_name in streamlit_tests.items():
                if test_key in content:
                    tests_found.append(f"Streamlit: {test_name}")
                    print(f"[OK] {test_name} (Streamlit)")
                else:
                    tests_missing.append(f"Streamlit: {test_name}")
    
    return tests_found, tests_missing

def check_descriptive_statistics():
    """Vérifie les statistiques descriptives."""
    print_header("VERIFICATION DES STATISTIQUES DESCRIPTIVES")
    
    stats_found = []
    
    # Vérifier dans streamlit_utils.py
    utils_file = Path('streamlit_utils.py')
    if utils_file.exists():
        with open(utils_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if 'describe()' in content:
                stats_found.append('Statistiques descriptives (describe)')
                print("[OK] Statistiques descriptives (describe)")
            
            if 'mean()' in content or '.mean()' in content:
                stats_found.append('Moyenne')
                print("[OK] Moyenne")
            
            if 'median()' in content or '.median()' in content:
                stats_found.append('Médiane')
                print("[OK] Médiane")
            
            if 'std()' in content or '.std()' in content:
                stats_found.append('Écart-type')
                print("[OK] Écart-type")
            
            if 'var()' in content or '.var()' in content:
                stats_found.append('Variance')
                print("[OK] Variance")
            
            if 'min()' in content or '.min()' in content:
                stats_found.append('Minimum')
                print("[OK] Minimum")
            
            if 'max()' in content or '.max()' in content:
                stats_found.append('Maximum')
                print("[OK] Maximum")
            
            if 'quantile' in content or '.quantile' in content:
                stats_found.append('Quantiles')
                print("[OK] Quantiles")
    
    return stats_found

def check_forecast_metrics():
    """Vérifie les métriques de prévision."""
    print_header("VERIFICATION DES METRIQUES DE PREVISION")
    
    metrics_found = []
    
    previsions_file = Path('app/blueprints/previsions/routes.py')
    if previsions_file.exists():
        with open(previsions_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if 'calculate_forecast_metrics' in content:
                print("[OK] Fonction calculate_forecast_metrics presente")
                metrics_found.append('Métriques de prévision')
            
            if 'historical_mean' in content:
                metrics_found.append('Moyenne historique')
                print("[OK] Moyenne historique")
            
            if 'historical_std' in content:
                metrics_found.append('Écart-type historique')
                print("[OK] Écart-type historique")
            
            if 'forecast_mean' in content:
                metrics_found.append('Moyenne des prévisions')
                print("[OK] Moyenne des prévisions")
            
            if 'forecast_range' in content:
                metrics_found.append('Plage des prévisions')
                print("[OK] Plage des prévisions")
            
            if 'confidence_range' in content:
                metrics_found.append('Intervalle de confiance')
                print("[OK] Intervalle de confiance")
    
    return metrics_found

def check_dependencies():
    """Vérifie les dépendances pour les statistiques."""
    print_header("VERIFICATION DES DEPENDANCES")
    
    dependencies = {
        'scipy': 'SciPy (tests statistiques)',
        'statsmodels': 'Statsmodels (modèles statistiques)',
        'numpy': 'NumPy (calculs numériques)',
        'pandas': 'Pandas (analyse de données)'
    }
    
    available = []
    missing = []
    
    for module, description in dependencies.items():
        try:
            __import__(module)
            available.append(description)
            print(f"[OK] {description}")
        except ImportError:
            missing.append(description)
            print(f"[ERREUR] {description} non installe")
    
    return available, missing

def check_visualizations():
    """Vérifie les visualisations statistiques."""
    print_header("VERIFICATION DES VISUALISATIONS STATISTIQUES")
    
    visualizations = []
    
    # Vérifier dans les routes de tests
    tests_file = Path('app/blueprints/tests/routes.py')
    if tests_file.exists():
        with open(tests_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if 'histogram' in content.lower():
                visualizations.append('Histogramme')
                print("[OK] Histogramme")
            
            if 'qqplot' in content.lower() or 'qq_plot' in content.lower():
                visualizations.append('QQ Plot')
                print("[OK] QQ Plot")
    
    # Vérifier dans page_visualisation.py
    viz_file = Path('pages/page_visualisation.py')
    if viz_file.exists():
        with open(viz_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if 'matrice_correlation' in content or 'correlation' in content:
                visualizations.append('Matrice de corrélation')
                print("[OK] Matrice de corrélation")
            
            if 'box' in content.lower() or 'moustache' in content.lower():
                visualizations.append('Boîte à moustaches')
                print("[OK] Boîte à moustaches")
    
    return visualizations

def main():
    """Fonction principale."""
    print("\n" + "=" * 70)
    print("VERIFICATION DES STATISTIQUES IMPLEMENTEES")
    print("=" * 70)
    
    # Vérifications
    tests_found, tests_missing = check_statistical_tests()
    desc_stats = check_descriptive_statistics()
    forecast_metrics = check_forecast_metrics()
    deps_available, deps_missing = check_dependencies()
    visualizations = check_visualizations()
    
    # Résumé
    print_header("RESUME")
    
    print(f"\n📊 Tests statistiques: {len(tests_found)} trouve(s)")
    print(f"📈 Statistiques descriptives: {len(desc_stats)} trouve(s)")
    print(f"🔮 Metriques de prevision: {len(forecast_metrics)} trouve(s)")
    print(f"📦 Dependances: {len(deps_available)}/{len(deps_available) + len(deps_missing)} installe(s)")
    print(f"📊 Visualisations: {len(visualizations)} trouve(s)")
    
    if deps_missing:
        print(f"\n⚠️  Dependances manquantes: {', '.join(deps_missing)}")
    
    total_features = len(tests_found) + len(desc_stats) + len(forecast_metrics) + len(visualizations)
    print(f"\n✅ Total: {total_features} fonctionnalites statistiques implementees")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

