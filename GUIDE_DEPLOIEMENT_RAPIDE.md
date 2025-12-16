# 🚀 Guide de Déploiement Rapide

## 📋 Prérequis

- ✅ Docker et Docker Compose installés
- ✅ Ports 80 et 443 disponibles
- ✅ Au moins 10GB d'espace disque libre

## 🎯 Déploiement en 3 Étapes

### Étape 1 : Générer le fichier .env

```bash
# Option A : Script automatique (recommandé)
python scripts/generate_env.py

# Option B : Manuel
cp ENV_EXAMPLE.txt .env
# Puis éditer .env et générer les valeurs :
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
python -c "import secrets; print('REDIS_PASSWORD=' + secrets.token_urlsafe(24))"
python -c "import secrets; print('POSTGRES_PASSWORD=' + secrets.token_urlsafe(24))"
```

### Étape 2 : Déployer

```bash
# Option A : Avec Makefile (recommandé)
make deploy

# Option B : Script bash
bash scripts/deploy.sh

# Option C : Manuel
docker-compose -f docs/docker-compose.prod.yml build
docker-compose -f docs/docker-compose.prod.yml up -d
```

### Étape 3 : Vérifier

```bash
# Vérifier la santé de l'application
make health
# ou
curl http://localhost/health

# Voir les logs
make logs

# Voir le statut des services
make status
```

## 🔍 Vérifications Post-Déploiement

### 1. Vérifier que tous les services sont démarrés

```bash
docker-compose -f docs/docker-compose.prod.yml ps
```

Vous devriez voir :
- ✅ `boursa_postgres` - running
- ✅ `boursa_redis` - running
- ✅ `boursa_app_1` - running (healthy)
- ✅ `boursa_app_2` - running (healthy)
- ✅ `boursa_app_3` - running (healthy)
- ✅ `boursa_nginx` - running

### 2. Vérifier les logs

```bash
# Logs de l'application
docker-compose -f docs/docker-compose.prod.yml logs flask_app_1

# Logs PostgreSQL
docker-compose -f docs/docker-compose.prod.yml logs postgres

# Logs Redis
docker-compose -f docs/docker-compose.prod.yml logs redis

# Logs Nginx
docker-compose -f docs/docker-compose.prod.yml logs nginx
```

### 3. Tester l'endpoint de santé

```bash
curl http://localhost/health
```

Réponse attendue :
```json
{
  "status": "healthy",
  "service": "boursa",
  "version": "1.0.0",
  "cache": "ok",
  "database": "ok"
}
```

### 4. Accéder à l'application

- **HTTP** : http://localhost
- **HTTPS** : https://localhost (si certificats configurés)

## 🛠️ Commandes Utiles

### Gestion des Services

```bash
make up          # Démarrer tous les services
make down        # Arrêter tous les services
make restart     # Redémarrer tous les services
make status      # Statut des services
make logs        # Voir les logs en temps réel
```

### Maintenance

```bash
make backup      # Créer une sauvegarde
make clean       # Nettoyer Docker
make health      # Vérifier la santé
```

### Base de Données

```bash
# Se connecter à PostgreSQL
docker exec -it boursa_postgres psql -U boursa_user -d boursa

# Vérifier les tables
docker exec -it boursa_postgres psql -U boursa_user -d boursa -c "\dt"

# Sauvegarder la base
docker exec boursa_postgres pg_dump -U boursa_user boursa > backup.sql
```

## ⚠️ Dépannage

### L'application ne démarre pas

1. **Vérifier les logs** :
   ```bash
   docker-compose -f docs/docker-compose.prod.yml logs
   ```

2. **Vérifier que .env existe** :
   ```bash
   ls -la .env
   ```

3. **Vérifier les variables d'environnement** :
   ```bash
   docker-compose -f docs/docker-compose.prod.yml config
   ```

### PostgreSQL ne démarre pas

```bash
# Vérifier les logs
docker-compose -f docs/docker-compose.prod.yml logs postgres

# Vérifier que POSTGRES_PASSWORD est défini dans .env
grep POSTGRES_PASSWORD .env
```

### Redis ne démarre pas

```bash
# Vérifier les logs
docker-compose -f docs/docker-compose.prod.yml logs redis

# Vérifier que REDIS_PASSWORD est défini dans .env
grep REDIS_PASSWORD .env
```

### Erreur "database is locked" (si SQLite)

Cela signifie que PostgreSQL n'est pas utilisé. Vérifiez :
```bash
# Vérifier DATABASE_URL dans .env
grep DATABASE_URL .env

# Vérifier que docker-compose utilise PostgreSQL
grep POSTGRES docker-compose.prod.yml
```

## 📊 Monitoring

### Vérifier l'utilisation des ressources

```bash
docker stats
```

### Vérifier l'espace disque

```bash
docker system df
```

### Vérifier les connexions actives

```bash
# PostgreSQL
docker exec boursa_postgres psql -U boursa_user -d boursa -c "SELECT count(*) FROM pg_stat_activity;"

# Redis
docker exec boursa_redis redis-cli -a $REDIS_PASSWORD INFO clients
```

## 🔒 Sécurité Post-Déploiement

1. ✅ Vérifier que `.env` n'est pas dans Git :
   ```bash
   git check-ignore .env
   ```

2. ✅ Changer le mot de passe admin par défaut :
   - Se connecter à l'application
   - Aller dans les paramètres utilisateur
   - Changer le mot de passe de l'admin

3. ✅ Configurer les certificats SSL :
   - Placer les certificats dans `nginx/ssl/`
   - Redémarrer Nginx : `docker-compose -f docs/docker-compose.prod.yml restart nginx`

## 🎉 Félicitations !

Votre application est maintenant déployée et fonctionnelle !

Pour plus d'informations, consultez :
- `docs/DEPLOIEMENT.md` - Guide détaillé
- `PRET_POUR_PRODUCTION.md` - Résumé complet
- `CHECKLIST_DEPLOIEMENT.md` - Checklist

---

**Besoin d'aide ?** Consultez les logs avec `make logs` ou vérifiez la documentation.

