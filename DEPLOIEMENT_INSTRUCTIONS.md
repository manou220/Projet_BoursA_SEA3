# 🚀 Instructions de Déploiement - Guide Pratique

## 📋 Étape 1 : Générer le fichier .env

### Option A : Script Python (Recommandé)

```bash
# Depuis le répertoire Projet-ML-Sea3/Projet-ML-Sea3
python scripts/generate_env.py
```

Le script va :
- ✅ Générer une SECRET_KEY sécurisée
- ✅ Générer des mots de passe pour Redis et PostgreSQL
- ✅ Créer le fichier .env avec toutes les valeurs

### Option B : Manuel

1. **Copier le template** :
   ```bash
   cp ENV_EXAMPLE.txt .env
   ```

2. **Générer SECRET_KEY** :
   ```bash
   python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
   ```
   Copiez la valeur générée dans `.env`

3. **Générer REDIS_PASSWORD** :
   ```bash
   python -c "import secrets; print('REDIS_PASSWORD=' + secrets.token_urlsafe(24))"
   ```
   Copiez la valeur générée dans `.env`

4. **Générer POSTGRES_PASSWORD** :
   ```bash
   python -c "import secrets; print('POSTGRES_PASSWORD=' + secrets.token_urlsafe(24))"
   ```
   Copiez la valeur générée dans `.env`

5. **Éditer .env** et remplacer toutes les valeurs `changez-moi-en-production`

## 📋 Étape 2 : Vérifier Docker

```bash
# Vérifier que Docker est installé
docker --version

# Vérifier que Docker Compose est installé
docker-compose --version
# ou
docker compose version
```

Si Docker n'est pas installé :
- **Windows** : Télécharger Docker Desktop depuis https://www.docker.com/products/docker-desktop
- **Linux** : `sudo apt-get install docker.io docker-compose`

## 📋 Étape 3 : Déployer

### Option A : Avec Makefile (si disponible)

```bash
make deploy
```

### Option B : Script Bash

```bash
bash scripts/deploy.sh
```

### Option C : Manuel

```bash
# 1. Construire les images
docker-compose -f docs/docker-compose.prod.yml build

# 2. Démarrer les services
docker-compose -f docs/docker-compose.prod.yml up -d

# 3. Vérifier le statut
docker-compose -f docs/docker-compose.prod.yml ps
```

## 📋 Étape 4 : Vérifier le Déploiement

### 1. Vérifier que tous les services sont démarrés

```bash
docker-compose -f docs/docker-compose.prod.yml ps
```

Vous devriez voir 6 services en état "Up" :
- `boursa_postgres`
- `boursa_redis`
- `boursa_app_1`
- `boursa_app_2`
- `boursa_app_3`
- `boursa_nginx`

### 2. Tester l'endpoint de santé

```bash
# Windows PowerShell
Invoke-WebRequest -Uri http://localhost/health

# Linux/Mac
curl http://localhost/health
```

Réponse attendue :
```json
{
  "status": "healthy",
  "service": "boursa",
  "cache": "ok",
  "database": "ok"
}
```

### 3. Vérifier les logs

```bash
# Tous les logs
docker-compose -f docs/docker-compose.prod.yml logs

# Logs d'une instance spécifique
docker-compose -f docs/docker-compose.prod.yml logs flask_app_1

# Logs en temps réel
docker-compose -f docs/docker-compose.prod.yml logs -f
```

### 4. Accéder à l'application

Ouvrez votre navigateur et allez sur :
- **http://localhost** (HTTP)
- **https://localhost** (HTTPS - si certificats configurés)

## 🔍 Vérifications Importantes

### Vérifier PostgreSQL

```bash
# Se connecter à PostgreSQL
docker exec -it boursa_postgres psql -U boursa_user -d boursa

# Dans psql, vérifier les tables
\dt

# Quitter
\q
```

### Vérifier Redis

```bash
# Tester Redis
docker exec -it boursa_redis redis-cli -a $REDIS_PASSWORD ping
# Devrait répondre : PONG
```

### Vérifier que les tables sont créées

```bash
# Initialiser la base si nécessaire
docker-compose -f docs/docker-compose.prod.yml run --rm flask_app_1 python scripts/init_db.py
```

## ⚠️ Problèmes Courants

### Erreur : "SECRET_KEY doit être défini"

**Solution** : Vérifiez que `.env` existe et contient `SECRET_KEY=...`

```bash
# Vérifier
cat .env | grep SECRET_KEY
```

### Erreur : "DATABASE_URL avec PostgreSQL est OBLIGATOIRE"

**Solution** : Les variables PostgreSQL doivent être définies dans `.env` :
- `POSTGRES_DB=boursa`
- `POSTGRES_USER=boursa_user`
- `POSTGRES_PASSWORD=votre-mot-de-passe`

### Erreur : "Port already in use"

**Solution** : Un autre service utilise les ports 80 ou 443.

```bash
# Windows
netstat -ano | findstr :80
netstat -ano | findstr :443

# Linux
sudo lsof -i :80
sudo lsof -i :443
```

Arrêtez le service qui utilise ces ports ou modifiez les ports dans `docker-compose.prod.yml`.

### Les conteneurs ne démarrent pas

```bash
# Voir les logs d'erreur
docker-compose -f docs/docker-compose.prod.yml logs

# Vérifier la configuration
docker-compose -f docs/docker-compose.prod.yml config
```

## 🎯 Commandes Rapides

```bash
# Démarrer
docker-compose -f docs/docker-compose.prod.yml up -d

# Arrêter
docker-compose -f docs/docker-compose.prod.yml down

# Redémarrer
docker-compose -f docs/docker-compose.prod.yml restart

# Voir les logs
docker-compose -f docs/docker-compose.prod.yml logs -f

# Statut
docker-compose -f docs/docker-compose.prod.yml ps

# Nettoyer
docker-compose -f docs/docker-compose.prod.yml down -v
```

## ✅ Checklist Finale

- [ ] Fichier `.env` créé et configuré
- [ ] Docker et Docker Compose installés
- [ ] Images Docker construites
- [ ] Tous les services démarrés
- [ ] Endpoint `/health` répond
- [ ] Application accessible via navigateur
- [ ] Logs sans erreurs critiques

## 🎉 Félicitations !

Si toutes les vérifications passent, votre application est déployée avec succès !

Pour plus d'informations :
- `GUIDE_DEPLOIEMENT_RAPIDE.md` - Guide rapide
- `docs/DEPLOIEMENT.md` - Guide détaillé
- `PRET_POUR_PRODUCTION.md` - Résumé complet

---

**Besoin d'aide ?** Consultez les logs avec `docker-compose -f docs/docker-compose.prod.yml logs`

