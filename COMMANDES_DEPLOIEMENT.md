# 🚀 Commandes de Déploiement - Guide Pratique

## 📍 Répertoire de Travail

Toutes les commandes doivent être exécutées depuis :
```
D:\emman\Desktop\Projet-ML-Sea3\Projet-ML-Sea3
```

## 🔧 Étape 1 : Générer le fichier .env

### Méthode Rapide (PowerShell)

```powershell
# Aller dans le répertoire du projet
cd "D:\emman\Desktop\Projet-ML-Sea3\Projet-ML-Sea3"

# Copier le template
Copy-Item ENV_EXAMPLE.txt .env

# Générer SECRET_KEY
$secretKey = python -c "import secrets; print(secrets.token_hex(32))"
(Get-Content .env) -replace 'SECRET_KEY=votre-cle-secrete-generee-ici-changez-moi', "SECRET_KEY=$secretKey" | Set-Content .env

# Générer REDIS_PASSWORD
$redisPwd = python -c "import secrets; print(secrets.token_urlsafe(24))"
(Get-Content .env) -replace 'REDIS_PASSWORD=changez-moi-en-production', "REDIS_PASSWORD=$redisPwd" | Set-Content .env

# Générer POSTGRES_PASSWORD
$postgresPwd = python -c "import secrets; print(secrets.token_urlsafe(24))"
(Get-Content .env) -replace 'POSTGRES_PASSWORD=changez-moi-en-production', "POSTGRES_PASSWORD=$postgresPwd" | Set-Content .env

Write-Host "Fichier .env cree avec succes!"
```

### Méthode Manuelle

1. **Copier le template** :
   ```powershell
   Copy-Item ENV_EXAMPLE.txt .env
   ```

2. **Ouvrir .env dans un éditeur** et remplacer :
   - `SECRET_KEY=votre-cle-secrete-generee-ici-changez-moi`
   - `REDIS_PASSWORD=changez-moi-en-production`
   - `POSTGRES_PASSWORD=changez-moi-en-production`

3. **Générer les valeurs** :
   ```powershell
   # SECRET_KEY
   python -c "import secrets; print(secrets.token_hex(32))"
   
   # REDIS_PASSWORD
   python -c "import secrets; print(secrets.token_urlsafe(24))"
   
   # POSTGRES_PASSWORD
   python -c "import secrets; print(secrets.token_urlsafe(24))"
   ```

## 🐳 Étape 2 : Vérifier Docker

```powershell
# Vérifier Docker
docker --version

# Vérifier Docker Compose
docker-compose --version
```

Si Docker n'est pas installé, téléchargez Docker Desktop depuis https://www.docker.com/products/docker-desktop

## 🚀 Étape 3 : Déployer

### Option A : Script de Déploiement

```powershell
# Depuis le répertoire Projet-ML-Sea3/Projet-ML-Sea3
bash scripts/deploy.sh
```

**Note** : Si bash n'est pas disponible sur Windows, utilisez l'option B ou C.

### Option B : Commandes Docker Compose Manuelles

```powershell
# 1. Construire les images
docker-compose -f docs/docker-compose.prod.yml build

# 2. Démarrer les services
docker-compose -f docs/docker-compose.prod.yml up -d

# 3. Vérifier le statut
docker-compose -f docs/docker-compose.prod.yml ps
```

### Option C : Avec Makefile (si make est installé)

```powershell
make deploy
```

## ✅ Étape 4 : Vérifier le Déploiement

### 1. Vérifier le statut des services

```powershell
docker-compose -f docs/docker-compose.prod.yml ps
```

Vous devriez voir 6 services :
- `boursa_postgres` - Up
- `boursa_redis` - Up  
- `boursa_app_1` - Up (healthy)
- `boursa_app_2` - Up (healthy)
- `boursa_app_3` - Up (healthy)
- `boursa_nginx` - Up

### 2. Tester l'endpoint de santé

```powershell
# PowerShell
Invoke-WebRequest -Uri http://localhost/health | Select-Object -ExpandProperty Content

# Ou avec curl si installé
curl http://localhost/health
```

Réponse attendue :
```json
{"status":"healthy","service":"boursa","version":"1.0.0","cache":"ok","database":"ok"}
```

### 3. Voir les logs

```powershell
# Tous les logs
docker-compose -f docs/docker-compose.prod.yml logs

# Logs d'une instance spécifique
docker-compose -f docs/docker-compose.prod.yml logs flask_app_1

# Logs en temps réel
docker-compose -f docs/docker-compose.prod.yml logs -f
```

### 4. Accéder à l'application

Ouvrez votre navigateur et allez sur :
- **http://localhost**

## 🔍 Commandes Utiles

### Gestion des Services

```powershell
# Démarrer
docker-compose -f docs/docker-compose.prod.yml up -d

# Arrêter
docker-compose -f docs/docker-compose.prod.yml down

# Redémarrer
docker-compose -f docs/docker-compose.prod.yml restart

# Voir le statut
docker-compose -f docs/docker-compose.prod.yml ps

# Voir les logs
docker-compose -f docs/docker-compose.prod.yml logs -f
```

### Base de Données

```powershell
# Se connecter à PostgreSQL
docker exec -it boursa_postgres psql -U boursa_user -d boursa

# Vérifier les tables (dans psql)
\dt

# Initialiser la base si nécessaire
docker-compose -f docs/docker-compose.prod.yml run --rm flask_app_1 python scripts/init_db.py
```

### Sauvegarde

```powershell
# Créer une sauvegarde
bash scripts/backup.sh

# Ou manuellement
docker exec boursa_postgres pg_dump -U boursa_user boursa > backup.sql
```

## ⚠️ Dépannage

### Erreur : "SECRET_KEY doit être défini"

```powershell
# Vérifier que .env existe
Test-Path .env

# Vérifier SECRET_KEY
Select-String -Path .env -Pattern "SECRET_KEY"
```

### Erreur : "Port already in use"

```powershell
# Vérifier les ports utilisés
netstat -ano | findstr :80
netstat -ano | findstr :443
```

### Les conteneurs ne démarrent pas

```powershell
# Voir les logs d'erreur
docker-compose -f docs/docker-compose.prod.yml logs

# Vérifier la configuration
docker-compose -f docs/docker-compose.prod.yml config
```

## 📋 Checklist Rapide

- [ ] Fichier `.env` créé avec SECRET_KEY, REDIS_PASSWORD, POSTGRES_PASSWORD
- [ ] Docker Desktop démarré
- [ ] Images construites : `docker-compose -f docs/docker-compose.prod.yml build`
- [ ] Services démarrés : `docker-compose -f docs/docker-compose.prod.yml up -d`
- [ ] Statut vérifié : `docker-compose -f docs/docker-compose.prod.yml ps`
- [ ] Health check OK : `Invoke-WebRequest http://localhost/health`
- [ ] Application accessible : http://localhost

## 🎉 C'est Prêt !

Une fois toutes les vérifications passées, votre application est déployée !

---

**Pour plus d'aide** : Consultez `DEPLOIEMENT_INSTRUCTIONS.md` ou `docs/DEPLOIEMENT.md`

