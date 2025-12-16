"""
Gestionnaires d'erreurs centralisés pour l'application Flask.
"""
from flask import render_template, jsonify, request
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """Enregistre les gestionnaires d'erreurs pour l'application."""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Gestionnaire pour les erreurs 400 (Bad Request)."""
        logger.warning(f"Bad Request: {request.url} - {str(error)}")
        if request.is_json or request.path.startswith('/api'):
            return jsonify({
                'error': 'Bad Request',
                'message': str(error.description) if hasattr(error, 'description') else 'Requête invalide',
                'status_code': 400
            }), 400
        return render_template('errors/400.html', error=error), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Gestionnaire pour les erreurs 401 (Unauthorized)."""
        logger.warning(f"Unauthorized: {request.url} - {str(error)}")
        if request.is_json or request.path.startswith('/api'):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentification requise',
                'status_code': 401
            }), 401
        return render_template('errors/401.html', error=error), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Gestionnaire pour les erreurs 403 (Forbidden)."""
        logger.warning(f"Forbidden: {request.url} - {str(error)}")
        if request.is_json or request.path.startswith('/api'):
            return jsonify({
                'error': 'Forbidden',
                'message': 'Accès refusé',
                'status_code': 403
            }), 403
        return render_template('errors/403.html', error=error), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Gestionnaire pour les erreurs 404 (Not Found)."""
        logger.info(f"Not Found: {request.url}")
        if request.is_json or request.path.startswith('/api'):
            return jsonify({
                'error': 'Not Found',
                'message': 'Ressource non trouvée',
                'status_code': 404
            }), 404
        return render_template('errors/404.html', error=error), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Gestionnaire pour les erreurs 429 (Rate Limit Exceeded)."""
        logger.warning(f"Rate Limit Exceeded: {request.url}")
        if request.is_json or request.path.startswith('/api'):
            return jsonify({
                'error': 'Rate Limit Exceeded',
                'message': 'Trop de requêtes. Veuillez réessayer plus tard.',
                'status_code': 429
            }), 429
        return render_template('errors/429.html', error=error), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        """Gestionnaire pour les erreurs 500 (Internal Server Error)."""
        logger.exception(f"Internal Server Error: {request.url} - {str(error)}")
        if request.is_json or request.path.startswith('/api'):
            # En production, ne pas exposer les détails de l'erreur
            message = 'Erreur serveur interne' if not app.config.get('DEBUG') else str(error)
            return jsonify({
                'error': 'Internal Server Error',
                'message': message,
                'status_code': 500
            }), 500
        return render_template('errors/500.html', error=error, debug=app.config.get('DEBUG')), 500
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """Gestionnaire pour les erreurs 503 (Service Unavailable)."""
        logger.error(f"Service Unavailable: {request.url} - {str(error)}")
        if request.is_json or request.path.startswith('/api'):
            return jsonify({
                'error': 'Service Unavailable',
                'message': 'Service temporairement indisponible',
                'status_code': 503
            }), 503
        return render_template('errors/503.html', error=error), 503
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Gestionnaire global pour toutes les exceptions non gérées."""
        logger.exception(f"Unhandled Exception: {request.url} - {type(error).__name__}: {str(error)}")
        
        # Si c'est une erreur HTTP connue, laisser Flask la gérer
        if hasattr(error, 'code'):
            raise error
        
        # Sinon, traiter comme une erreur 500
        if request.is_json or request.path.startswith('/api'):
            message = 'Erreur serveur interne' if not app.config.get('DEBUG') else str(error)
            return jsonify({
                'error': 'Internal Server Error',
                'message': message,
                'status_code': 500
            }), 500
        
        return render_template('errors/500.html', error=error, debug=app.config.get('DEBUG')), 500

