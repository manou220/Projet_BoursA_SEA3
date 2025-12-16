# 🪟 Guide de Déploiement pour Windows

## 📋 Prérequis

- ✅ Docker Desktop installé et démarré
- ✅ Python 3.x installé
- ✅ PowerShell 5.1+ ou PowerShell Core

## 🚀 Déploiement en 3 Étapes

### Étape 1 : Générer le fichier .env

**Option A : Script PowerShell (Recommandé)**

```powershell
# Aller dans le répertoire du projet
cd "D:\emman\Desktop\Projet-ML-Sea3\Projet-ML-Sea3"

# Exécuter le script
.\scripts\generate_env.ps1
```

**Option B : Manuel**

```powershell
# 1. Copier le template
Copy-Item ENV_EXAMPLE.txt .env

# 2. Générer SECRET_KEY
$secretKey = python -c "import secrets; print(secrets.token_hex(32))"
(Get-Content .env) -replace 'SECRET_KEY=votre-cle-secrete-generee-ici-changez-moi', "SECRET_KEY=$secretKey" | Set-Content .env

# 3. Générer REDIS_PASSWORD
$redisPwd = python -c "import secrets; print(secrets.token_urlsafe(24))"
(Get-Content .env) -replace 'REDIS_PASSWORD=changez-moi-en-production', "REDIS_PASSWORD=$redisPwd" | Set-Content .env

# 4. Générer POSTGRES_PASSWORD
$postgresPwd = python -c "import secrets; print(secrets.token_urlsafe(24))"
(Get-Content .env) -replace 'POSTGRES_PASSWORD=changez-moi-en-production', "POSTGRES_PASSWORD=$postgresPwd" | Set-Content .env

Write-Host "Fichier .env cree avec succes!"
```

### Étape 2 : Vérifier Docker

```powershell
# Vérifier que Docker Desktop est démarré
docker --version
docker-compose --version

# Si Docker n'est pas installé, téléchargez Docker Desktop :
# https://www.docker.com/products/docker-desktop
```

### Étape 3 : Déployer

```powershell
# Depuis le répertoire Projet-ML-Sea3/Projet-ML-Sea3

# 1. Construire les images
docker-compose -f docs/docker-compose.prod.yml build

# 2. Démarrer les services
docker-compose -f docs/docker-compose.prod.yml up -d

# 3. Vérifier le statut
docker-compose -f docs/docker-compose.prod.yml ps
```

## ✅ Vérifications

### 1. Vérifier que tous les services sont démarrés

```powershell
docker-compose -f docs/docker-compose.prod.yml ps
```

Vous devriez voir 6 services en état "Up" :
- `boursa_postgres`
- `boursa_redis`
- `boursa_app_1` (healthy)
- `boursa_app_2` (healthy)
- `boursa_app_3` (healthy)
- `boursa_nginx`

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

# Logs en temps réel (Ctrl+C pour arrêter)
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

# Initialiser la base si nécessaire
docker-compose -f docs/docker-compose.prod.yml run --rm flask_app_1 python scripts/init_db.py
```

## ⚠️ Dépannage Windows

### Erreur : "docker-compose : command not found"

**Solution** : Utilisez `docker compose` (sans tiret) :
```powershell
docker compose -f docs/docker-compose.prod.yml up -d
```

### Erreur : "Port already in use"

```powershell
# Vérifier les ports utilisés
netstat -ano | findstr :80
netstat -ano | findstr :443

# Trouver le processus utilisant le port
netstat -ano | findstr :80 | findstr LISTENING
```

### Docker Desktop ne démarre pas

1. Vérifier que la virtualisation est activée dans le BIOS
2. Vérifier que WSL2 est installé (Windows 10/11)
3. Redémarrer Docker Desktop

### Les conteneurs ne démarrent pas

```powershell
# Voir les logs d'erreur
docker-compose -f docs/docker-compose.prod.yml logs

# Vérifier la configuration
docker-compose -f docs/docker-compose.prod.yml config
```

## 📋 Checklist Windows

- [ ] Docker Desktop installé et démarré
- [ ] Python installé (pour générer les secrets)
- [ ] Fichier `.env` créé avec toutes les valeurs
- [ ] Images Docker construites
- [ ] Services démarrés
- [ ] Health check répond
- [ ] Application accessible via navigateur

## 🎉 C'est Prêt !

Une fois toutes les vérifications passées, votre application est déployée !

---

**Pour plus d'aide** : Consultez `COMMANDES_DEPLOIEMENT.md` ou `docs/DEPLOIEMENT.md`

