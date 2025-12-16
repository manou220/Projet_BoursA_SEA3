# 🗄️ Guide : Utilisation de votre Base de Données SQL Existante

## 📋 Vue d'Ensemble

Ce guide vous explique comment configurer et utiliser votre base de données SQL (PostgreSQL ou MySQL) existante avec ce projet Flask.

---

## ✅ Étape 1 : Identifier votre Base de Données

### Type de Base de Données

**PostgreSQL** (recommandé) :
- ✅ Support complet
- ✅ Meilleures performances avec plusieurs instances
- ✅ Fonctionnalités avancées

**MySQL/MariaDB** :
- ✅ Supporté via `mysql+pymysql://`
- ⚠️ Nécessite `pymysql` installé

### Informations Requises

Vous devez avoir :
- ✅ **Host** : Adresse du serveur (ex: `localhost`, `db.example.com`)
- ✅ **Port** : Port de la base (PostgreSQL: `5432`, MySQL: `3306`)
- ✅ **Database** : Nom de la base de données
- ✅ **Username** : Nom d'utilisateur
- ✅ **Password** : Mot de passe

---

## 🔧 Étape 2 : Configuration dans `.env`

### Format de la DATABASE_URL

**PostgreSQL** :
```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
```

**MySQL** :
```bash
DATABASE_URL=mysql+pymysql://username:password@host:port/database_name
```

### Exemples Concrets

#### Exemple 1 : PostgreSQL Local
```bash
DATABASE_URL=postgresql://boursa_user:mon_mot_de_passe@localhost:5432/boursa_db
```

#### Exemple 2 : PostgreSQL Distant
```bash
DATABASE_URL=postgresql://boursa_user:mon_mot_de_passe@192.168.1.100:5432/boursa_db
```

#### Exemple 3 : PostgreSQL avec SSL
```bash
DATABASE_URL=postgresql://boursa_user:mon_mot_de_passe@db.example.com:5432/boursa_db?sslmode=require
```

#### Exemple 4 : MySQL
```bash
DATABASE_URL=mysql+pymysql://boursa_user:mon_mot_de_passe@localhost:3306/boursa_db
```

### Configuration Complète dans `.env`

Créez ou modifiez votre fichier `.env` à la racine du projet :

```bash
# ============================================
# BASE DE DONNÉES (OBLIGATOIRE)
# ============================================
# Remplacez par vos informations réelles
DATABASE_URL=postgresql://votre_user:votre_password@votre_host:5432/votre_database
SQLALCHEMY_DATABASE_URI=postgresql://votre_user:votre_password@votre_host:5432/votre_database

# ============================================
# ENVIRONNEMENT
# ============================================
FLASK_ENV=production
APP_CONFIG=production

# ============================================
# SÉCURITÉ (OBLIGATOIRE)
# ============================================
# Générer avec: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=votre-cle-secrete-generee-ici

# ============================================
# REDIS (Recommandé pour la production)
# ============================================
CACHE_TYPE=Redis
CACHE_REDIS_URL=redis://:votre_mot_de_passe@redis:6379/0

# ============================================
# DOCKER COMPOSE (si utilisé)
# ============================================
POSTGRES_DB=boursa
POSTGRES_USER=boursa_user
POSTGRES_PASSWORD=votre_mot_de_passe
REDIS_PASSWORD=votre_mot_de_passe_redis
```

---

## 🚀 Étape 3 : Tester la Connexion

### Test Rapide

```bash
# Test de connexion simple
python -c "
from app import create_app
from app.extensions import db
app = create_app()
with app.app_context():
    try:
        result = db.session.execute(db.text('SELECT 1')).scalar()
        print('✅ Connexion à la base de données réussie!')
    except Exception as e:
        print(f'❌ Erreur de connexion: {e}')
"
```

### Test avec Script

Créez un fichier `test_db_connection.py` :

```python
#!/usr/bin/env python3
"""Test de connexion à la base de données."""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    try:
        # Test de connexion
        result = db.session.execute(db.text('SELECT 1')).scalar()
        print('✅ Connexion réussie!')
        
        # Afficher les informations de connexion (sans mot de passe)
        db_url = app.config.get('SQLALCHEMY_DATABASE_URI', 'Non configuré')
        # Masquer le mot de passe
        if '@' in db_url:
            parts = db_url.split('@')
            if ':' in parts[0]:
                user_pass = parts[0].split('://')[1]
                if ':' in user_pass:
                    user = user_pass.split(':')[0]
                    db_url_safe = db_url.replace(user_pass, f'{user}:***')
                    print(f'📊 Base de données: {db_url_safe}')
        
        # Lister les tables existantes
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f'📋 Tables existantes: {len(tables)}')
        for table in tables:
            print(f'   - {table}')
            
    except Exception as e:
        print(f'❌ Erreur: {e}')
        sys.exit(1)
```

Exécutez :
```bash
python test_db_connection.py
```

---

## 📦 Étape 4 : Initialiser les Tables

### Création des Tables

Une fois la connexion testée, créez les tables nécessaires :

```bash
python scripts/init_db.py
```

Ce script va :
1. ✅ Créer toutes les tables nécessaires :
   - `users` : Utilisateurs et authentification
   - `data_files` : Métadonnées des fichiers uploadés
   - `test_history` : Historique des tests statistiques
   - `user_locations` : Localisations pour la cartographie
2. ✅ Initialiser les données de base (utilisateur admin, localisations d'exemple)
3. ✅ Vérifier que tout fonctionne

### Vérification

Après l'initialisation, vérifiez :

```bash
# Vérifier les tables
python -c "
from app import create_app
from app.extensions import db
app = create_app()
with app.app_context():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    expected = ['users', 'data_files', 'test_history', 'user_locations']
    for table in expected:
        status = '✅' if table in tables else '❌'
        print(f'{status} {table}')
"
```

---

## 🔄 Étape 5 : Migration depuis SQLite (Optionnel)

Si vous avez des données dans SQLite à migrer :

### Préparation

1. **Sauvegarder SQLite** :
```bash
cp user_locations.db user_locations.db.backup
```

2. **Configurer les variables** :
```bash
export DATABASE_URL=postgresql://user:password@host:5432/dbname
export SQLITE_DB_PATH=user_locations.db
```

3. **Exécuter la migration** :
```bash
python scripts/migrate_to_postgresql.py
```

### Vérification Post-Migration

```bash
# Compter les enregistrements
python -c "
from app import create_app
from app.models.user_location import UserLocation
app = create_app()
with app.app_context():
    count = UserLocation.query.count()
    print(f'✅ {count} localisations migrées')
"
```

---

## 🐳 Étape 6 : Configuration Docker (si utilisé)

### Option A : Utiliser votre Base de Données Externe

Si votre base de données est **en dehors de Docker** :

1. **Modifier `docker-compose.prod.yml`** :
   - Supprimer le service `postgres`
   - Utiliser `host.docker.internal` ou l'IP de votre serveur

2. **Configuration dans `.env`** :
```bash
# Pour accéder à une base de données sur l'hôte depuis Docker
DATABASE_URL=postgresql://user:password@host.docker.internal:5432/dbname

# Ou avec l'IP du serveur
DATABASE_URL=postgresql://user:password@192.168.1.100:5432/dbname
```

3. **Réseau Docker** :
   - Si la base est sur un autre serveur, assurez-vous que le port est accessible
   - Vérifiez les règles de firewall

### Option B : Utiliser PostgreSQL dans Docker

Si vous voulez créer PostgreSQL dans Docker :

1. **Décommenter le service `postgres` dans `docker-compose.prod.yml`**
2. **Configurer dans `.env`** :
```bash
POSTGRES_DB=boursa
POSTGRES_USER=boursa_user
POSTGRES_PASSWORD=votre_mot_de_passe
DATABASE_URL=postgresql://boursa_user:votre_mot_de_passe@postgres:5432/boursa
```

---

## ✅ Étape 7 : Vérification Finale

### Checklist

- [ ] Connexion testée avec succès
- [ ] Tables créées (`python scripts/init_db.py`)
- [ ] Health check fonctionne (`curl http://localhost/health`)
- [ ] Application démarre sans erreur
- [ ] Données accessibles depuis l'application

### Test Complet

```bash
# 1. Test de connexion
python test_db_connection.py

# 2. Initialisation
python scripts/init_db.py

# 3. Health check
curl http://localhost/health

# 4. Démarrer l'application
python app_main.py
# ou
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

---

## 🔧 Dépannage

### Erreur : "database does not exist"

**Solution** : Créer la base de données :
```sql
-- PostgreSQL
CREATE DATABASE boursa_db;

-- MySQL
CREATE DATABASE boursa_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Erreur : "password authentication failed"

**Solution** : Vérifier le mot de passe dans `DATABASE_URL`

### Erreur : "connection refused"

**Solution** : 
- Vérifier que le serveur PostgreSQL/MySQL est démarré
- Vérifier le port (5432 pour PostgreSQL, 3306 pour MySQL)
- Vérifier les règles de firewall

### Erreur : "relation does not exist"

**Solution** : Exécuter `python scripts/init_db.py` pour créer les tables

### Erreur : "psycopg2 not installed"

**Solution** : Installer le driver PostgreSQL
```bash
pip install psycopg2-binary
```

Pour MySQL :
```bash
pip install pymysql
```

---

## 📊 Tables Créées

Le script `init_db.py` crée les tables suivantes :

1. **`users`** : Utilisateurs et authentification
   - `id`, `username`, `email`, `password_hash`, `role`, `created_at`

2. **`data_files`** : Métadonnées des fichiers uploadés
   - `id`, `filename`, `original_filename`, `file_path`, `file_size`, `uploaded_at`, `user_id`

3. **`test_history`** : Historique des tests statistiques
   - `id`, `test_name`, `filename`, `columns_used`, `p_value`, `stat_value`, `interpretation`, `full_results`, `timestamp`, `user_id`

4. **`user_locations`** : Localisations pour la cartographie
   - `id`, `username`, `latitude`, `longitude`, `active_users`, `timestamp`

---

## 🎯 Prochaines Étapes

Une fois votre base de données configurée :

1. ✅ Tester toutes les fonctionnalités de l'application
2. ✅ Vérifier que les données persistent correctement
3. ✅ Configurer les sauvegardes automatiques
4. ✅ Mettre en place le monitoring

---

## 📞 Support

Si vous rencontrez des problèmes :

1. Vérifiez les logs : `docker-compose logs -f` (si Docker)
2. Testez la connexion : `python test_db_connection.py`
3. Consultez `PROBLEMES_DEPLOIEMENT.md` pour les problèmes connus
4. Vérifiez la configuration dans `.env`

---

*Guide créé pour l'intégration de votre base de données SQL existante*


