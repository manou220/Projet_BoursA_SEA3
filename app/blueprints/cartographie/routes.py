"""
Blueprint pour la cartographie et la capture de positions en temps réel.
"""

from flask import Blueprint, render_template, current_app, request, jsonify
from app.extensions import cache, db
from app.utils import get_real_time_users_from_db, save_user_location
from app.models.user_location import UserLocation

bp = Blueprint('cartographie', __name__)


@bp.route('/')
@cache.cached(timeout=60)  # Cache court (1 min) car données en temps réel
def index():
    """Affiche la carte interactive."""
    # Utiliser SQLAlchemy si disponible, sinon fallback vers utils
    try:
        user_data = [loc.to_dict() for loc in UserLocation.get_all_locations()]
    except Exception:
        # Fallback vers l'ancienne méthode
        db_path = current_app.config.get('DB_PATH', 'user_locations.db')
        user_data = get_real_time_users_from_db(db_path)
    
    return render_template("cartographie.html", initial_locations=user_data)


@bp.route('/api/locations', methods=['GET', 'POST'])
def locations_api():
    """API REST pour récupérer ou enregistrer les positions utilisateurs."""
    db_path = current_app.config.get('DB_PATH', 'user_locations.db')
    cache_key = f'locations_api_{db_path}'

    if request.method == 'GET':
        # Cache très court pour les données en temps réel (15 secondes)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return jsonify({"users": cached_data})
        
        # Utiliser SQLAlchemy si disponible
        try:
            user_data = [loc.to_dict() for loc in UserLocation.get_all_locations()]
        except Exception:
            # Fallback vers l'ancienne méthode
            user_data = get_real_time_users_from_db(db_path)
        
        cache.set(cache_key, user_data, timeout=15)
        return jsonify({"users": user_data})

    payload = request.get_json(silent=True) or {}
    username = (payload.get('username') or 'Visiteur').strip() or 'Visiteur'
    lat = payload.get('lat') if 'lat' in payload else payload.get('latitude')
    lon = payload.get('lon') if 'lon' in payload else payload.get('longitude')
    active_users = payload.get('active_users', 1)

    if lat is None or lon is None:
        return jsonify({"error": "Latitude et longitude sont requises"}), 400

    try:
        lat = float(lat)
        lon = float(lon)
        active_users = int(active_users) if active_users is not None else 1
    except (TypeError, ValueError):
        return jsonify({"error": "Latitude/longitude invalides"}), 400

    try:
        # Utiliser SQLAlchemy si disponible
        try:
            UserLocation.save_or_update(username, lat, lon, active_users)
        except Exception:
            # Fallback vers l'ancienne méthode
            save_user_location(db_path, username, lat, lon, active_users)
        
        # Invalider le cache après une mise à jour
        cache.delete(cache_key)
    except Exception as exc:
        current_app.logger.exception("Impossible d'enregistrer la position", exc_info=exc)
        return jsonify({"error": "Erreur lors de l'enregistrement"}), 500

    return jsonify({"status": "ok"})
