"""
Blueprint pour les pages principales de l'application.
"""
from flask import render_template, Blueprint
from app.extensions import cache

bp = Blueprint('home', __name__)


@bp.route('/')
@bp.route('/accueil')
@cache.cached(timeout=300)  # Cache 5 minutes
def accueil():
    """Page d'accueil de l'application."""
    return render_template("accueil.html")


@bp.route('/description')
@cache.cached(timeout=600)  # Cache 10 minutes (page moins fréquente)
def description():
    """Page de description de l'application et des tests."""
    return render_template("description.html")


@bp.route('/health')
def health():
    """Endpoint de health check pour le monitoring et load balancer."""
    from flask import jsonify
    from app.extensions import cache, db
    import os
    
    health_status = {
        'status': 'healthy',
        'service': 'boursa',
        'version': '1.0.0'
    }
    
    # Vérifier le cache (Redis si configuré)
    try:
        cache.set('health_check', 'ok', timeout=10)
        cache_status = cache.get('health_check')
        health_status['cache'] = 'ok' if cache_status == 'ok' else 'degraded'
    except Exception as e:
        health_status['cache'] = 'error'
        health_status['cache_error'] = str(e)
    
    # Vérifier la base de données
    try:
        db.session.execute(db.text('SELECT 1'))
        health_status['database'] = 'ok'
    except Exception as e:
        health_status['database'] = 'error'
        health_status['database_error'] = str(e)
    
    # Déterminer le statut global
    if health_status['cache'] == 'error' or health_status['database'] == 'error':
        health_status['status'] = 'degraded'
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    
    return jsonify(health_status), status_code