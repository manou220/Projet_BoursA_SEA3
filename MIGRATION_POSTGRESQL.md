# 🔄 Migration vers PostgreSQL - Guide Complet

## ⚠️ PROBLÈME IDENTIFIÉ

**SQLite est INAPPROPRIÉ pour votre architecture de production** car :

1. ❌ **3 instances Flask** → Conflits de verrous SQLite
2. ❌ **Pas de concurrence** → Erreurs "database is locked"
3. ❌ **Pas de réplication** → Point de défaillance unique
4. ❌ **Sauvegardes difficiles** → Risque de corruption

## ✅ SOLUTION : PostgreSQL

PostgreSQL est maintenant **configuré et requis** pour la production.

## 📋 Étapes de Migration

### 1. Mettre à Jour les Variables d'Environnement

Ajouter dans `.env` :

```bash
# Base de données PostgreSQL (OBLIGATOIRE en production)
DATABASE_URL=postgresql://boursa_user:votre-mot-de-passe@postgres:5432/boursa

# Variables pour Docker Compose
POSTGRES_DB=boursa
POSTGRES_USER=boursa_user
POSTGRES_PASSWORD=votre-mot-de-passe-fort
```

### 2. Démarrer PostgreSQL avec Docker Compose

```bash
# Démarrer uniquement PostgreSQL d'abord
docker-compose -f docs/docker-compose.prod.yml up -d postgres

# Attendre que PostgreSQL soit prêt
docker-compose -f docs/docker-compose.prod.yml logs postgres
```

### 3. Créer les Tables avec SQLAlchemy

```bash
# Démarrer une instance Flask temporaire pour créer les tables
docker-compose -f docs/docker-compose.prod.yml run --rm flask_app_1 python -c "
from app import create_app
app = create_app('production')
with app.app_context():
    from app.extensions import db
    from app.models.user import init_users_table
    from app.models.data_file import DataFile
    from app.models.test_history import TestHistory
    db.create_all()
    init_users_table()
    print('✅ Tables créées')
"
```

### 4. Migrer les Données SQLite (si existantes)

Si vous avez des données dans SQLite :

```bash
# Installer psycopg2 si nécessaire
pip install psycopg2-binary

# Exécuter le script de migration
export DATABASE_URL=postgresql://boursa_user:password@localhost:5432/boursa
export SQLITE_DB_PATH=user_locations.db
python scripts/migrate_to_postgresql.py
```

### 5. Migrer les Données `user_locations`

Les données de localisation utilisateur (`user_locations`) utilisent sqlite3 directement. 

**Option A : Créer un modèle SQLAlchemy** (recommandé)

Créer `app/models/user_location.py` :

```python
from app.extensions import db
from datetime import datetime

class UserLocation(db.Model):
    __tablename__ = 'user_locations'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, index=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    active_users = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            'username': self.username,
            'lat': self.latitude,
            'lon': self.longitude,
            'active_users': self.active_users,
            'timestamp': self.timestamp.isoformat()
        }
```

Puis modifier `app/utils.py` pour utiliser SQLAlchemy au lieu de sqlite3.

**Option B : Script de migration manuel**

```python
# scripts/migrate_user_locations.py
import sqlite3
import psycopg2
from urllib.parse import urlparse

sqlite_conn = sqlite3.connect('user_locations.db')
cursor = sqlite_conn.cursor()
cursor.execute("SELECT * FROM user_locations")
rows = cursor.fetchall()

postgres_url = "postgresql://user:password@localhost:5432/boursa"
parsed = urlparse(postgres_url)
pg_conn = psycopg2.connect(
    host=parsed.hostname,
    port=parsed.port or 5432,
    database=parsed.path[1:],
    user=parsed.username,
    password=parsed.password
)

pg_cursor = pg_conn.cursor()
for row in rows:
    pg_cursor.execute(
        "INSERT INTO user_locations (username, latitude, longitude, active_users, timestamp) VALUES (%s, %s, %s, %s, %s)",
        row
    )

pg_conn.commit()
pg_cursor.close()
pg_conn.close()
sqlite_conn.close()
```

### 6. Vérifier la Migration

```bash
# Se connecter à PostgreSQL
docker exec -it boursa_postgres psql -U boursa_user -d boursa

# Vérifier les tables
\dt

# Vérifier les données
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM user_locations;
```

### 7. Démarrer l'Application Complète

```bash
# Démarrer tous les services
docker-compose -f docs/docker-compose.prod.yml up -d

# Vérifier les logs
docker-compose -f docs/docker-compose.prod.yml logs -f flask_app_1
```

## 🔍 Vérifications Post-Migration

1. ✅ Vérifier que les 3 instances Flask démarrent sans erreur
2. ✅ Tester l'authentification utilisateur
3. ✅ Vérifier que les données sont accessibles
4. ✅ Tester les fonctionnalités (upload, tests, prévisions)

## 📊 Avantages de PostgreSQL

- ✅ **Concurrence** : Des milliers de connexions simultanées
- ✅ **Performance** : Optimisé pour les applications multi-utilisateurs
- ✅ **Fiabilité** : ACID complet, transactions robustes
- ✅ **Sauvegardes** : pg_dump, WAL archiving, sauvegardes en ligne
- ✅ **Réplication** : Master-slave pour haute disponibilité
- ✅ **Monitoring** : Outils avancés (pg_stat, pgAdmin)

## 🛠️ Maintenance PostgreSQL

### Sauvegardes

```bash
# Sauvegarde complète
docker exec boursa_postgres pg_dump -U boursa_user boursa > backup_$(date +%Y%m%d).sql

# Restauration
docker exec -i boursa_postgres psql -U boursa_user boursa < backup_20250101.sql
```

### Monitoring

```bash
# Voir les connexions actives
docker exec boursa_postgres psql -U boursa_user -d boursa -c "SELECT count(*) FROM pg_stat_activity;"

# Voir la taille de la base
docker exec boursa_postgres psql -U boursa_user -d boursa -c "SELECT pg_size_pretty(pg_database_size('boursa'));"
```

## ⚠️ Notes Importantes

1. **SQLite reste disponible pour le développement** si DATABASE_URL n'est pas défini
2. **PostgreSQL est OBLIGATOIRE en production** (vérifié dans ProductionConfig)
3. **Les modèles SQLAlchemy sont compatibles** avec PostgreSQL sans modification
4. **Les requêtes sqlite3 directes** doivent être migrées vers SQLAlchemy

## 🎯 Résultat

Après migration, votre application sera :
- ✅ Prête pour la production
- ✅ Supportant plusieurs instances Flask
- ✅ Avec haute disponibilité
- ✅ Avec sauvegardes fiables

---

**Date** : Décembre 2025  
**Statut** : Migration requise avant déploiement production

