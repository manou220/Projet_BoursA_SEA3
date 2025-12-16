# 🚀 Guide de Déploiement sur Render - BoursA

Guide complet pour déployer votre application BoursA sur Render.

## ✅ Vérification de la Configuration

### Fichiers Requis (Tous Présents ✅)

- ✅ **Dockerfile** - Configuré pour utiliser la variable PORT
- ✅ **wsgi.py** - Point d'entrée WSGI correct
- ✅ **requirements.txt** - Toutes les dépendances
- ✅ **render.yaml** - Configuration Render
- ✅ **app/__init__.py** - Application Flask
- ✅ **app/config.py** - Configuration avec support DATABASE_URL

### Configuration Dockerfile ✅

Le Dockerfile a été mis à jour pour:
- ✅ Utiliser la variable `PORT` de Render (ou 5000 par défaut)
- ✅ Health check adapté pour Render
- ✅ Commande Gunicorn dynamique

---

## 📋 Étapes de Déploiement

### 1. Créer un Compte Render

1. Aller sur [render.com](https://render.com)
2. Cliquer sur "Get Started for Free"
3. Créer un compte (GitHub, Google, ou email)

### 2. Connecter votre Repository

1. Dans le dashboard Render, cliquer sur "New +"
2. Sélectionner "Web Service"
3. Connecter votre repository GitHub/GitLab/Bitbucket
4. Sélectionner le repository contenant BoursA

### 3. Configurer le Service Web

Render détecte automatiquement `render.yaml`, mais vous pouvez aussi configurer manuellement:

**Configuration de Base:**
- **Name**: `boursa-app` (ou votre choix)
- **Environment**: `Docker`
- **Region**: Choisir la région la plus proche de vos utilisateurs
- **Branch**: `main` (ou votre branche principale)
- **Root Directory**: Laisser vide (racine du projet)

**Build & Deploy:**
- **Build Command**: Laisser vide (Docker gère tout)
- **Start Command**: Laisser vide (défini dans Dockerfile)

### 4. Créer le Service PostgreSQL

1. Dans le dashboard, cliquer sur "New +"
2. Sélectionner "PostgreSQL"
3. Configuration:
   - **Name**: `boursa-postgres`
   - **Database**: `boursa`
   - **User**: `boursa_user`
   - **Plan**: `Starter` (gratuit) ou `Standard` ($7/mois)
   - **Region**: Même région que le service web

### 5. Créer le Service Redis (Optionnel mais Recommandé)

1. Dans le dashboard, cliquer sur "New +"
2. Sélectionner "Redis"
3. Configuration:
   - **Name**: `boursa-redis`
   - **Plan**: `Starter` (gratuit) ou `Standard` ($10/mois)
   - **Region**: Même région que le service web

### 6. Configurer les Variables d'Environnement

Dans le service web (`boursa-app`), aller dans "Environment" et ajouter:

#### Variables Obligatoires

```env
FLASK_ENV=production
APP_CONFIG=production
SECRET_KEY=<générer avec: python -c "import secrets; print(secrets.token_hex(32))">
```

#### Variables Automatiques (Render les génère)

Ces variables sont automatiquement injectées par Render:
- `DATABASE_URL` - Depuis le service PostgreSQL
- `REDIS_URL` - Depuis le service Redis (si créé)
- `PORT` - Port sur lequel l'application doit écouter

#### Variables Optionnelles

```env
CACHE_TYPE=Redis
LOG_LEVEL=INFO
USE_HTTPS=true
DISABLE_PUBLIC_REGISTRATION=false
ALPHAVANTAGE_KEY=<votre-clé-si-vous-en-avez-une>
IEX_CLOUD_API_KEY=<votre-clé-si-vous-en-avez-une>
```

#### Configuration Redis

Si vous avez créé un service Redis, configurer:

```env
CACHE_REDIS_URL=${REDIS_URL}
```

Ou si Render fournit `REDIS_URL` directement, l'utiliser dans votre code.

### 7. Lier les Services

1. Dans le service web, aller dans "Environment"
2. Cliquer sur "Link Resource"
3. Sélectionner `boursa-postgres`
4. Render ajoute automatiquement `DATABASE_URL`
5. Répéter pour `boursa-redis` si créé

### 8. Déployer

1. Cliquer sur "Manual Deploy" → "Deploy latest commit"
2. Attendre que le build se termine (5-10 minutes la première fois)
3. Vérifier les logs pour s'assurer qu'il n'y a pas d'erreurs

---

## 🔍 Vérification Post-Déploiement

### 1. Vérifier les Logs

Dans le dashboard Render, aller dans "Logs" du service web:
- Vérifier qu'il n'y a pas d'erreurs
- Chercher "Application initialisée en mode production"
- Vérifier que la base de données est connectée

### 2. Tester l'Application

1. Cliquer sur l'URL fournie par Render (ex: `boursa-app.onrender.com`)
2. Tester le health check: `https://boursa-app.onrender.com/health`
3. Vérifier que l'application répond correctement

### 3. Initialiser la Base de Données

Si c'est la première fois, vous devrez peut-être initialiser les tables:

**Option A: Via les logs Render**
- Les logs montreront si l'initialisation a réussi

**Option B: Via un script**
- Créer un service "Shell" temporaire dans Render
- Exécuter: `python scripts/init_db.py`

---

## ⚙️ Configuration Avancée

### Custom Domain

1. Dans le service web, aller dans "Settings"
2. Section "Custom Domains"
3. Ajouter votre domaine
4. Suivre les instructions DNS

### Auto-Deploy

Par défaut, Render déploie automatiquement à chaque push sur la branche principale.

Pour désactiver:
- Settings → Auto-Deploy → Désactiver

### Health Checks

Render vérifie automatiquement `/health` toutes les minutes.

Pour personnaliser:
- Settings → Health Check Path → `/health` (déjà configuré)

### Scaling

Pour augmenter les ressources:
- Settings → Plan → Choisir un plan supérieur

---

## 🐛 Dépannage

### Erreur: "Port already in use"

**Solution**: Le Dockerfile utilise maintenant `${PORT:-5000}`, ce problème ne devrait plus se produire.

### Erreur: "Database connection failed"

**Vérifications**:
1. Le service PostgreSQL est démarré
2. `DATABASE_URL` est défini dans les variables d'environnement
3. Les services sont liés (Link Resource)

**Solution**: Vérifier que `DATABASE_URL` est bien injecté par Render.

### Erreur: "SECRET_KEY not set"

**Solution**: Ajouter `SECRET_KEY` dans les variables d'environnement du service web.

### Erreur: "Redis connection failed"

**Vérifications**:
1. Le service Redis est créé
2. `REDIS_URL` ou `CACHE_REDIS_URL` est défini
3. Les services sont liés

**Solution**: Si Redis n'est pas critique, vous pouvez désactiver le cache Redis temporairement en mettant `CACHE_TYPE=SimpleCache`.

### Build échoue

**Vérifications**:
1. Les logs de build pour voir l'erreur exacte
2. `requirements.txt` est à jour
3. Le Dockerfile est correct

**Solution**: Vérifier les logs de build dans Render.

---

## 📊 Coûts Render

### Plan Gratuit (Free Tier)

- **Web Service**: 750 heures/mois (peut s'endormir après 15 min d'inactivité)
- **PostgreSQL**: 90 jours gratuits, puis $7/mois
- **Redis**: 30 jours gratuits, puis $10/mois

### Plan Starter (Recommandé pour Production)

- **Web Service**: $7/mois (pas de sleep)
- **PostgreSQL**: $7/mois
- **Redis**: $10/mois
- **Total**: ~$24/mois

---

## ✅ Checklist de Déploiement

Avant de déployer:

- [ ] Compte Render créé
- [ ] Repository connecté
- [ ] Service web créé
- [ ] Service PostgreSQL créé
- [ ] Service Redis créé (optionnel)
- [ ] Services liés (Link Resource)
- [ ] Variables d'environnement configurées:
  - [ ] `SECRET_KEY`
  - [ ] `FLASK_ENV=production`
  - [ ] `APP_CONFIG=production`
  - [ ] `DATABASE_URL` (automatique)
  - [ ] `REDIS_URL` (automatique si Redis créé)
- [ ] Déploiement réussi
- [ ] Health check fonctionne (`/health`)
- [ ] Application accessible

---

## 🎯 Prochaines Étapes

1. **Déployer** en suivant ce guide
2. **Tester** l'application
3. **Configurer un domaine personnalisé** (optionnel)
4. **Mettre en place des sauvegardes** (automatiques avec PostgreSQL Standard)
5. **Monitorer** les performances via les logs Render

---

## 📚 Ressources

- [Documentation Render](https://render.com/docs)
- [Render Docker Guide](https://render.com/docs/docker)
- [Render Environment Variables](https://render.com/docs/environment-variables)
- [Render PostgreSQL](https://render.com/docs/databases)

---

**Date de mise à jour**: Décembre 2025  
**Statut**: ✅ **PRÊT POUR LE DÉPLOIEMENT SUR RENDER**

