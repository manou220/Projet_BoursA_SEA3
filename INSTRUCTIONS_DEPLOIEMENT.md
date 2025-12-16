# ✅ Instructions de Déploiement - État Actuel

## ✅ Vérifications Effectuées

- ✅ **Fichier .env** : Existe et contient toutes les valeurs nécessaires
  - SECRET_KEY : ✅ Configuré
  - POSTGRES_PASSWORD : ✅ Configuré  
  - REDIS_PASSWORD : ✅ Configuré

## ⚠️ Action Requise : Démarrer Docker Desktop

**Docker Desktop n'est pas démarré.** Vous devez le démarrer avant de continuer.

### Étapes :

1. **Ouvrir Docker Desktop**
   - Cherchez "Docker Desktop" dans le menu Démarrer
   - Cliquez pour l'ouvrir
   - Attendez que l'icône dans la barre des tâches indique "Docker Desktop is running"

2. **Vérifier que Docker fonctionne**
   ```powershell
   docker ps
   ```
   Si cette commande fonctionne (affiche une liste, même vide), Docker est prêt.

## 🚀 Une fois Docker Desktop Démarré

Exécutez ces commandes **dans l'ordre** depuis PowerShell :

```powershell
# Aller dans le répertoire du projet
cd "D:\emman\Desktop\Projet-ML-Sea3\Projet-ML-Sea3"

# 1. Construire les images Docker
docker-compose -f docs/docker-compose.prod.yml build

# 2. Démarrer tous les services
docker-compose -f docs/docker-compose.prod.yml up -d

# 3. Vérifier le statut
docker-compose -f docs/docker-compose.prod.yml ps

# 4. Tester la santé de l'application
Invoke-WebRequest -Uri http://localhost/health | Select-Object -ExpandProperty Content
```

## ⏱️ Temps Estimé

- **Build des images** : 5-10 minutes (première fois)
- **Démarrage des services** : 1-2 minutes
- **Total** : ~10-15 minutes

## 📊 Résultat Attendu

Après le déploiement, vous devriez voir :

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

## 🔍 En Cas de Problème

### Docker Desktop ne démarre pas
- Vérifiez que la virtualisation est activée dans le BIOS
- Redémarrez votre ordinateur si nécessaire
- Réinstallez Docker Desktop si le problème persiste

### Erreur lors du build
```powershell
# Voir les logs détaillés
docker-compose -f docs/docker-compose.prod.yml build --no-cache
```

### Erreur lors du démarrage
```powershell
# Voir les logs
docker-compose -f docs/docker-compose.prod.yml logs

# Vérifier la configuration
docker-compose -f docs/docker-compose.prod.yml config
```

## 📝 Checklist

- [x] Fichier .env créé avec toutes les valeurs
- [ ] Docker Desktop démarré
- [ ] Images Docker construites
- [ ] Services démarrés
- [ ] Health check OK
- [ ] Application accessible

---

**Prochaine étape** : Démarrer Docker Desktop, puis exécuter les commandes ci-dessus.

