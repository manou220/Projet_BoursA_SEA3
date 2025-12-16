# ✅ PRÊT À DÉPLOYER - Commandes à Exécuter Maintenant

## ✅ Vérifications Préalables

✅ **Docker installé** : Docker version 29.1.2  
✅ **Docker Compose installé** : v2.40.3  
✅ **Répertoire** : `D:\emman\Desktop\Projet-ML-Sea3\Projet-ML-Sea3`

## 🚀 Commandes à Exécuter (Dans l'Ordre)

### 1️⃣ Générer le fichier .env

**Exécutez cette commande PowerShell** :

```powershell
cd "D:\emman\Desktop\Projet-ML-Sea3\Projet-ML-Sea3"
.\scripts\generate_env.ps1
```

**OU** si le script ne fonctionne pas, exécutez ces commandes :

```powershell
cd "D:\emman\Desktop\Projet-ML-Sea3\Projet-ML-Sea3"
Copy-Item ENV_EXAMPLE.txt .env
$sk = python -c "import secrets; print(secrets.token_hex(32))"
(Get-Content .env) -replace 'SECRET_KEY=votre-cle-secrete-generee-ici-changez-moi', "SECRET_KEY=$sk" | Set-Content .env
$rp = python -c "import secrets; print(secrets.token_urlsafe(24))"
(Get-Content .env) -replace 'REDIS_PASSWORD=changez-moi-en-production', "REDIS_PASSWORD=$rp" | Set-Content .env
$pp = python -c "import secrets; print(secrets.token_urlsafe(24))"
(Get-Content .env) -replace 'POSTGRES_PASSWORD=changez-moi-en-production', "POSTGRES_PASSWORD=$pp" | Set-Content .env
Write-Host "Fichier .env cree avec succes!" -ForegroundColor Green
```

### 2️⃣ Construire les Images Docker

```powershell
cd "D:\emman\Desktop\Projet-ML-Sea3\Projet-ML-Sea3"
docker-compose -f docs/docker-compose.prod.yml build
```

⏱️ **Temps estimé** : 5-10 minutes (première fois)

### 3️⃣ Démarrer les Services

```powershell
docker-compose -f docs/docker-compose.prod.yml up -d
```

⏱️ **Temps estimé** : 1-2 minutes

### 4️⃣ Vérifier le Statut

```powershell
docker-compose -f docs/docker-compose.prod.yml ps
```

**Résultat attendu** : 6 services en état "Up"

### 5️⃣ Tester la Santé de l'Application

```powershell
Invoke-WebRequest -Uri http://localhost/health | Select-Object -ExpandProperty Content
```

**Résultat attendu** :
```json
{"status":"healthy","service":"boursa","version":"1.0.0","cache":"ok","database":"ok"}
```

### 6️⃣ Accéder à l'Application

Ouvrez votre navigateur et allez sur :
- **http://localhost**

## 📊 Vérifications Post-Déploiement

### Vérifier les Logs

```powershell
# Logs de l'application
docker-compose -f docs/docker-compose.prod.yml logs flask_app_1

# Tous les logs
docker-compose -f docs/docker-compose.prod.yml logs
```

### Vérifier PostgreSQL

```powershell
# Se connecter à PostgreSQL
docker exec -it boursa_postgres psql -U boursa_user -d boursa

# Dans psql, vérifier les tables
\dt

# Quitter
\q
```

### Initialiser la Base de Données (si nécessaire)

```powershell
docker-compose -f docs/docker-compose.prod.yml run --rm flask_app_1 python scripts/init_db.py
```

## 🎯 Commandes Utiles

```powershell
# Arrêter tous les services
docker-compose -f docs/docker-compose.prod.yml down

# Redémarrer tous les services
docker-compose -f docs/docker-compose.prod.yml restart

# Voir les logs en temps réel
docker-compose -f docs/docker-compose.prod.yml logs -f

# Nettoyer Docker
docker system prune -f
```

## ⚠️ En Cas de Problème

### Erreur : "SECRET_KEY doit être défini"

```powershell
# Vérifier que .env existe
Test-Path .env

# Vérifier SECRET_KEY
Select-String -Path .env -Pattern "SECRET_KEY"
```

### Erreur : "Port already in use"

```powershell
# Vérifier les ports
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

## ✅ Checklist Finale

- [ ] Fichier `.env` créé avec SECRET_KEY, REDIS_PASSWORD, POSTGRES_PASSWORD
- [ ] Images Docker construites
- [ ] Services démarrés (6 services Up)
- [ ] Health check répond avec "healthy"
- [ ] Application accessible sur http://localhost
- [ ] Logs sans erreurs critiques

## 🎉 Félicitations !

Si toutes les vérifications passent, votre application est déployée avec succès !

---

**Documentation complète** :
- `DEMARRAGE_RAPIDE.md` - Guide rapide
- `DEPLOIEMENT_WINDOWS.md` - Guide Windows détaillé
- `docs/DEPLOIEMENT.md` - Guide complet

