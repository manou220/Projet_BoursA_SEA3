# ⚡ Démarrage Rapide - Commandes Exactes

## 🎯 Vous êtes ici : `D:\emman\Desktop\Projet-ML-Sea3\Projet-ML-Sea3`

## 📋 Étape 1 : Générer le fichier .env

### Option A : Script PowerShell (Recommandé)

```powershell
.\scripts\generate_env.ps1
```

### Option B : Commandes Manuelles

```powershell
# Copier le template
Copy-Item ENV_EXAMPLE.txt .env

# Générer et remplacer SECRET_KEY
$sk = python -c "import secrets; print(secrets.token_hex(32))"
(Get-Content .env) -replace 'SECRET_KEY=votre-cle-secrete-generee-ici-changez-moi', "SECRET_KEY=$sk" | Set-Content .env

# Générer et remplacer REDIS_PASSWORD
$rp = python -c "import secrets; print(secrets.token_urlsafe(24))"
(Get-Content .env) -replace 'REDIS_PASSWORD=changez-moi-en-production', "REDIS_PASSWORD=$rp" | Set-Content .env

# Générer et remplacer POSTGRES_PASSWORD
$pp = python -c "import secrets; print(secrets.token_urlsafe(24))"
(Get-Content .env) -replace 'POSTGRES_PASSWORD=changez-moi-en-production', "POSTGRES_PASSWORD=$pp" | Set-Content .env

Write-Host "Fichier .env cree!" -ForegroundColor Green
```

## 📋 Étape 2 : Vérifier Docker

```powershell
# Vérifier Docker
docker --version

# Vérifier Docker Compose
docker-compose --version
# ou
docker compose version
```

**Si Docker n'est pas installé** : Téléchargez Docker Desktop depuis https://www.docker.com/products/docker-desktop

## 📋 Étape 3 : Déployer

```powershell
# Construire les images Docker
docker-compose -f docs/docker-compose.prod.yml build

# Démarrer tous les services
docker-compose -f docs/docker-compose.prod.yml up -d

# Vérifier le statut
docker-compose -f docs/docker-compose.prod.yml ps
```

## 📋 Étape 4 : Vérifier

```powershell
# Tester l'endpoint de santé
Invoke-WebRequest -Uri http://localhost/health | Select-Object -ExpandProperty Content

# Voir les logs
docker-compose -f docs/docker-compose.prod.yml logs -f flask_app_1
```

## ✅ Résultat Attendu

Si tout fonctionne, vous devriez voir :

1. **6 services démarrés** :
   ```
   boursa_postgres    Up
   boursa_redis       Up
   boursa_app_1       Up (healthy)
   boursa_app_2       Up (healthy)
   boursa_app_3       Up (healthy)
   boursa_nginx       Up
   ```

2. **Health check OK** :
   ```json
   {"status":"healthy","service":"boursa","cache":"ok","database":"ok"}
   ```

3. **Application accessible** : http://localhost

## 🔍 Commandes de Vérification

```powershell
# Statut des services
docker-compose -f docs/docker-compose.prod.yml ps

# Logs en temps réel
docker-compose -f docs/docker-compose.prod.yml logs -f

# Health check
Invoke-WebRequest http://localhost/health

# Arrêter les services
docker-compose -f docs/docker-compose.prod.yml down

# Redémarrer
docker-compose -f docs/docker-compose.prod.yml restart
```

## ⚠️ Si ça ne fonctionne pas

1. **Vérifier Docker Desktop** : Est-il démarré ?
2. **Vérifier .env** : Le fichier existe-t-il ? Contient-il SECRET_KEY, REDIS_PASSWORD, POSTGRES_PASSWORD ?
3. **Voir les logs** : `docker-compose -f docs/docker-compose.prod.yml logs`
4. **Vérifier les ports** : Les ports 80 et 443 sont-ils libres ?

## 📚 Documentation Complète

- `DEPLOIEMENT_WINDOWS.md` - Guide Windows détaillé
- `COMMANDES_DEPLOIEMENT.md` - Toutes les commandes
- `docs/DEPLOIEMENT.md` - Guide complet

---

**Prêt ?** Exécutez les commandes ci-dessus dans l'ordre ! 🚀

