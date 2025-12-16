# 🚀 Guide de Déploiement Complet - BoursA

Ce guide vous accompagne dans le déploiement de l'application BoursA en production.

## 📋 Table des Matières

1. [Prérequis](#prérequis)
2. [Configuration Initiale](#configuration-initiale)
3. [Déploiement avec Docker](#déploiement-avec-docker)
4. [Déploiement sans Docker](#déploiement-sans-docker)
5. [Configuration SSL/HTTPS](#configuration-sslhttps)
6. [Maintenance et Monitoring](#maintenance-et-monitoring)
7. [Sauvegarde et Restauration](#sauvegarde-et-restauration)
8. [Dépannage](#dépannage)

---

## 📦 Prérequis

### Système

- **OS**: Linux (Ubuntu 20.04+ recommandé), macOS, ou Windows avec WSL2
- **RAM**: Minimum 2GB, recommandé 4GB+
- **Disque**: Minimum 10GB d'espace libre
- **CPU**: 2 cœurs minimum

### Logiciels

- **Docker**: Version 20.10+
- **Docker Compose**: Version 1.29+ (ou Docker Compose V2)
- **Git**: Pour cloner le repository
- **OpenSSL**: Pour générer les certificats SSL (déjà installé sur la plupart des systèmes)

### Vérification

```bash
# Vérifier Docker
docker --version
docker-compose --version  # ou: docker compose version

# Vérifier Git
git --version

# Vérifier OpenSSL
openssl version
```

---

## ⚙️ Configuration Initiale

### 1. Cloner le Repository

```bash
git clone <votre-repository-url>
cd Projet-ML-Sea3/Projet-ML-Sea3
```

### 2. Créer le Fichier .env

```bash
# Copier le fichier d'exemple
cp ENV_EXAMPLE.txt .env

# Éditer le fichier .env avec vos valeurs
nano .env  # ou vim, code, etc.
```

### 3. Variables d'Environnement Obligatoires

```bash
# Clé secrète Flask (OBLIGATOIRE)
# Générer avec: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=votre-cle-secrete-generee-ici

# Base de données PostgreSQL
POSTGRES_DB=boursa
POSTGRES_USER=boursa_user
POSTGRES_PASSWORD=votre-mot-de-passe-securise

# Redis (optionnel mais recommandé)
REDIS_PASSWORD=votre-mot-de-passe-redis

# Environnement
FLASK_ENV=production
APP_CONFIG=production
```

### 4. Variables d'Environnement Optionnelles

```bash
# Cache Redis
CACHE_TYPE=Redis
CACHE_REDIS_URL=redis://:votre-mot-de-passe-redis@redis:6379/0

# APIs Boursières (optionnel)
ALPHAVANTAGE_KEY=votre-cle-alpha-vantage
IEX_CLOUD_API_KEY=votre-cle-iex-cloud

# Logging
LOG_LEVEL=INFO

# HTTPS
USE_HTTPS=true
```

---

## 🐳 Déploiement avec Docker

### Option 1: Déploiement Automatisé (Recommandé)

```bash
# Rendre le script exécutable
chmod +x scripts/deploy.sh

# Déployer en production
./scripts/deploy.sh production

# Ou en développement
./scripts/deploy.sh development
```

### Option 2: Déploiement Manuel

```bash
# 1. Construire les images
docker-compose build

# 2. Démarrer les services
docker-compose up -d

# 3. Vérifier les logs
docker-compose logs -f

# 4. Vérifier le statut
docker-compose ps
```

### Services Disponibles

Après le déploiement, les services sont disponibles sur:

- **Application Flask**: http://localhost:5000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Nginx** (si activé): http://localhost:80, https://localhost:443

### Activer Nginx

```bash
# Démarrer avec le profil nginx
docker-compose --profile nginx up -d
```

---

## 🖥️ Déploiement sans Docker

### 1. Installer les Dépendances Système

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib redis-server nginx

# macOS (avec Homebrew)
brew install python@3.11 postgresql redis nginx
```

### 2. Créer l'Environnement Virtuel

```bash
python3.11 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurer PostgreSQL

```bash
# Créer la base de données
sudo -u postgres psql
CREATE DATABASE boursa;
CREATE USER boursa_user WITH PASSWORD 'votre-mot-de-passe';
GRANT ALL PRIVILEGES ON DATABASE boursa TO boursa_user;
\q
```

### 4. Initialiser la Base de Données

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Initialiser la base de données
python scripts/init_db.py
```

### 5. Démarrer l'Application

```bash
# Avec Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - wsgi:app

# Ou avec Flask (développement uniquement)
export FLASK_ENV=development
python app_main.py
```

---

## 🔒 Configuration SSL/HTTPS

### Option 1: Certificats Auto-signés (Développement)

```bash
# Générer les certificats
chmod +x scripts/generate_ssl_certs.sh
./scripts/generate_ssl_certs.sh localhost

# Les certificats seront créés dans nginx/ssl/
```

### Option 2: Let's Encrypt (Production)

```bash
# Installer Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtenir un certificat
sudo certbot --nginx -d votre-domaine.com

# Le certificat sera automatiquement renouvelé
```

### Configuration Nginx avec SSL

Les certificats doivent être placés dans `nginx/ssl/`:
- `cert.pem`: Certificat
- `key.pem`: Clé privée

---

## 🔧 Maintenance et Monitoring

### Vérifier le Statut des Services

```bash
# Statut des conteneurs
docker-compose ps

# Logs en temps réel
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f flask_app
```

### Health Check

```bash
# Vérifier la santé de l'application
curl http://localhost:5000/health

# Réponse attendue:
# {
#   "status": "healthy",
#   "service": "boursa",
#   "version": "1.0.0",
#   "cache": "ok",
#   "database": "ok"
# }
```

### Redémarrer les Services

```bash
# Redémarrer tous les services
docker-compose restart

# Redémarrer un service spécifique
docker-compose restart flask_app
```

### Mettre à Jour l'Application

```bash
# 1. Arrêter les services
docker-compose down

# 2. Mettre à jour le code
git pull

# 3. Reconstruire les images
docker-compose build

# 4. Redémarrer les services
docker-compose up -d
```

---

## 💾 Sauvegarde et Restauration

### Sauvegarde Automatique

```bash
# Rendre le script exécutable
chmod +x scripts/backup.sh

# Créer une sauvegarde
./scripts/backup.sh

# Les sauvegardes sont stockées dans ./backups/
```

### Restauration

```bash
# Rendre le script exécutable
chmod +x scripts/restore.sh

# Restaurer depuis une sauvegarde
./scripts/restore.sh ./backups/backup_20250101_120000
```

### Sauvegarde Manuelle

```bash
# Sauvegarder la base de données
docker exec boursa_postgres pg_dump -U boursa_user boursa > backup.sql

# Sauvegarder les uploads
tar -czf uploads_backup.tar.gz uploads/

# Sauvegarder les modèles ML
tar -czf models_backup.tar.gz app/models/
```

---

## 🔍 Dépannage

### Problèmes Courants

#### 1. L'application ne démarre pas

```bash
# Vérifier les logs
docker-compose logs flask_app

# Vérifier les variables d'environnement
docker-compose exec flask_app env | grep -E "SECRET_KEY|DATABASE_URL"
```

#### 2. Erreur de connexion à la base de données

```bash
# Vérifier que PostgreSQL est démarré
docker-compose ps postgres

# Tester la connexion
docker-compose exec postgres psql -U boursa_user -d boursa -c "SELECT 1;"
```

#### 3. Erreur de connexion à Redis

```bash
# Vérifier que Redis est démarré
docker-compose ps redis

# Tester la connexion
docker-compose exec redis redis-cli ping
```

#### 4. Certificats SSL invalides

```bash
# Régénérer les certificats
./scripts/generate_ssl_certs.sh votre-domaine.com
```

#### 5. Port déjà utilisé

```bash
# Vérifier les ports utilisés
netstat -tulpn | grep -E "5000|5432|6379|80|443"

# Modifier les ports dans docker-compose.yml ou .env
```

### Commandes Utiles

```bash
# Entrer dans un conteneur
docker-compose exec flask_app bash

# Voir les ressources utilisées
docker stats

# Nettoyer les images inutilisées
docker system prune -a

# Voir les volumes
docker volume ls
```

---

## 📚 Ressources Supplémentaires

- [Documentation Docker](https://docs.docker.com/)
- [Documentation Docker Compose](https://docs.docker.com/compose/)
- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [Documentation Redis](https://redis.io/documentation)
- [Documentation Nginx](https://nginx.org/en/docs/)

---

## ✅ Checklist de Déploiement

Avant de mettre en production:

- [ ] Fichier `.env` créé et configuré
- [ ] `SECRET_KEY` généré et sécurisé
- [ ] `POSTGRES_PASSWORD` fort et sécurisé
- [ ] `REDIS_PASSWORD` configuré (si utilisé)
- [ ] Base de données PostgreSQL créée
- [ ] Certificats SSL configurés (pour HTTPS)
- [ ] Firewall configuré (ports 80, 443, 5000)
- [ ] Sauvegarde automatique configurée
- [ ] Monitoring configuré
- [ ] Logs configurés et accessibles
- [ ] Tests de santé effectués
- [ ] Documentation à jour

---

**Date de dernière mise à jour**: Décembre 2025  
**Version**: 1.0.0

