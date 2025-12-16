"""
Modèle SQLAlchemy pour les localisations utilisateur.
Remplace l'utilisation directe de sqlite3.
"""
from app.extensions import db
from datetime import datetime


class UserLocation(db.Model):
    """Modèle pour stocker les localisations des utilisateurs."""
    __tablename__ = 'user_locations'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, index=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    active_users = db.Column(db.Integer, default=1, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour JSON."""
        return {
            'username': self.username,
            'lat': self.latitude,
            'lon': self.longitude,
            'active_users': self.active_users,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    def __repr__(self):
        return f'<UserLocation {self.username} ({self.latitude}, {self.longitude})>'
    
    @classmethod
    def get_all_locations(cls):
        """Récupère toutes les localisations."""
        return cls.query.all()
    
    @classmethod
    def get_by_username(cls, username):
        """Récupère la localisation d'un utilisateur."""
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def save_or_update(cls, username, latitude, longitude, active_users=1):
        """Enregistre ou met à jour la localisation d'un utilisateur."""
        location = cls.query.filter_by(username=username).first()
        
        if location:
            # Mettre à jour
            location.latitude = latitude
            location.longitude = longitude
            location.active_users = active_users
            location.timestamp = datetime.utcnow()
        else:
            # Créer
            location = cls(
                username=username,
                latitude=latitude,
                longitude=longitude,
                active_users=active_users
            )
            db.session.add(location)
        
        db.session.commit()
        return location

