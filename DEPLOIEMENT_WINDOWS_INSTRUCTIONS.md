# 🪟 Instructions de Déploiement Windows

## ⚠️ Prérequis

Avant de déployer, assurez-vous que:

1. **Docker Desktop est installé et démarré**
   - Ouvrez Docker Desktop depuis le menu Démarrer
   - Attendez que l'icône Docker dans la barre des tâches soit verte
   - Vérifiez avec: `docker ps` (ne doit pas donner d'erreur)

2. **Le fichier .env est configuré**
   - Le fichier `.env` existe déjà
   - Vérifiez qu'il contient au minimum:
     - `SECRET_KEY` (généré)
     - `POSTGRES_PASSWORD` (mot de passe fort)
     - `REDIS_PASSWORD` (optionnel)

## 🚀 Déploiement

### Option 1: Script PowerShell (Recommandé)

```powershell
# Dans PowerShell, depuis le répertoire du projet
.\scripts\deploy.ps1 production
```

### Option 2: Docker Compose Manuel

```powershell
# 1. Construire les images
docker compose build

# 2. Démarrer les services
docker compose up -d

# 3. Vérifier les logs
docker compose logs -f
```

### Option 3: Makefile (si disponible)

```powershell
make build
make up
```

## 🔍 Vérification

```powershell
# Vérifier que les conteneurs sont en cours d'exécution
docker compose ps

# Vérifier la santé de l'application
Invoke-WebRequest -Uri "http://localhost:5000/health"

# Voir les logs
docker compose logs -f flask_app
```

## 🆘 Problèmes Courants

### Docker Desktop n'est pas démarré

**Erreur**: `failed to connect to the docker API`

**Solution**:
1. Ouvrez Docker Desktop depuis le menu Démarrer
2. Attendez que l'icône soit verte dans la barre des tâches
3. Réessayez la commande

### Port déjà utilisé

**Erreur**: `port is already allocated`

**Solution**: Modifiez les ports dans `.env`:
```env
APP_PORT=5001
POSTGRES_PORT=5433
REDIS_PORT=6380
```

### Variables d'environnement manquantes

**Erreur**: `The "POSTGRES_PASSWORD" variable is not set`

**Solution**: Ajoutez les variables dans `.env`:
```env
POSTGRES_PASSWORD=votre-mot-de-passe-fort
REDIS_PASSWORD=votre-mot-de-passe-redis
```

## 📝 Commandes Utiles

```powershell
# Arrêter les services
docker compose down

# Redémarrer les services
docker compose restart

# Voir les logs
docker compose logs -f

# Nettoyer
docker compose down -v
docker system prune -a
```

