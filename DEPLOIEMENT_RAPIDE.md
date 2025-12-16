# 🚀 Déploiement Rapide - BoursA

Guide de démarrage rapide pour déployer BoursA en 5 minutes.

## ⚡ Déploiement Express

### 1. Préparer l'environnement

```bash
# Créer le fichier .env
cp ENV_EXAMPLE.txt .env

# Générer une SECRET_KEY
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> .env

# Éditer .env et définir:
# - POSTGRES_PASSWORD (mot de passe fort)
# - REDIS_PASSWORD (optionnel)
```

### 2. Déployer avec Docker

```bash
# Option A: Script automatisé (recommandé)
chmod +x scripts/deploy.sh
./scripts/deploy.sh production

# Option B: Makefile
make setup-env  # Créer .env si nécessaire
make build
make up

# Option C: Docker Compose manuel
docker-compose build
docker-compose up -d
```

### 3. Vérifier le déploiement

```bash
# Vérifier les services
docker-compose ps

# Vérifier la santé
curl http://localhost:5000/health

# Voir les logs
docker-compose logs -f
```

### 4. Accéder à l'application

- **Application**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

---

## 🔧 Commandes Utiles

```bash
# Voir les logs
make logs
# ou
docker-compose logs -f

# Redémarrer
make restart

# Arrêter
make down

# Sauvegarder
make backup
# ou
./scripts/backup.sh

# Maintenance
./scripts/maintenance.sh health
```

---

## 📝 Configuration Minimale (.env)

```bash
# Obligatoire
SECRET_KEY=votre-cle-secrete-generee
POSTGRES_PASSWORD=votre-mot-de-passe
FLASK_ENV=production

# Optionnel
REDIS_PASSWORD=votre-mot-de-passe-redis
ALPHAVANTAGE_KEY=votre-cle-api
IEX_CLOUD_API_KEY=votre-cle-api
```

---

## ⚠️ Problèmes Courants

### Port déjà utilisé

Modifier dans `.env`:
```bash
APP_PORT=5001
POSTGRES_PORT=5433
REDIS_PORT=6380
```

### Erreur de connexion à la base de données

Vérifier que PostgreSQL est démarré:
```bash
docker-compose ps postgres
docker-compose logs postgres
```

### Certificats SSL manquants (pour Nginx)

```bash
chmod +x scripts/generate_ssl_certs.sh
./scripts/generate_ssl_certs.sh localhost
```

---

## 📚 Documentation Complète

Pour plus de détails, consultez:
- [GUIDE_DEPLOIEMENT_COMPLET.md](./GUIDE_DEPLOIEMENT_COMPLET.md)
- [README.md](./README.md)

---

**Temps estimé**: 5-10 minutes  
**Difficulté**: Facile

