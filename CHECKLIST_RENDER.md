# ✅ Checklist de Déploiement Render - BoursA

## 📋 Vérification Pré-Déploiement

### Fichiers Requis ✅

- [x] **Dockerfile** - ✅ Configuré pour utiliser PORT
- [x] **wsgi.py** - ✅ Point d'entrée WSGI
- [x] **requirements.txt** - ✅ Toutes les dépendances
- [x] **render.yaml** - ✅ Configuration Render
- [x] **app/__init__.py** - ✅ Application Flask
- [x] **app/config.py** - ✅ Support REDIS_URL et DATABASE_URL

### Configuration ✅

- [x] Dockerfile utilise `${PORT:-5000}` au lieu de port fixe
- [x] Health check adapté pour Render
- [x] render.yaml configuré correctement
- [x] Support REDIS_URL de Render dans config.py

---

## 🚀 Étapes de Déploiement

### 1. Préparation

- [ ] Compte Render créé
- [ ] Repository GitHub/GitLab/Bitbucket prêt
- [ ] Code poussé sur la branche principale

### 2. Création des Services

- [ ] Service Web créé
  - [ ] Nom: `boursa-app`
  - [ ] Runtime: Docker
  - [ ] Branch: `main` (ou votre branche)
  
- [ ] Service PostgreSQL créé
  - [ ] Nom: `boursa-postgres`
  - [ ] Database: `boursa`
  - [ ] User: `boursa_user`
  
- [ ] Service Redis créé (optionnel)
  - [ ] Nom: `boursa-redis`

### 3. Configuration

- [ ] Services liés (Link Resource)
  - [ ] PostgreSQL lié au service web
  - [ ] Redis lié au service web (si créé)

- [ ] Variables d'environnement configurées:
  - [ ] `SECRET_KEY` (généré)
  - [ ] `FLASK_ENV=production`
  - [ ] `APP_CONFIG=production`
  - [ ] `DATABASE_URL` (automatique via Link Resource)
  - [ ] `REDIS_URL` (automatique via Link Resource si Redis créé)
  - [ ] `CACHE_TYPE=Redis` (si Redis utilisé)
  - [ ] `LOG_LEVEL=INFO`
  - [ ] `USE_HTTPS=true`

### 4. Déploiement

- [ ] Build réussi (vérifier les logs)
- [ ] Déploiement réussi
- [ ] Aucune erreur dans les logs

### 5. Vérification Post-Déploiement

- [ ] Application accessible via l'URL Render
- [ ] Health check fonctionne: `/health`
- [ ] Base de données initialisée
- [ ] Pas d'erreurs dans les logs
- [ ] Application répond correctement

---

## 🔍 Tests à Effectuer

- [ ] Accéder à la page d'accueil
- [ ] Tester le health check: `https://votre-app.onrender.com/health`
- [ ] Vérifier la connexion à la base de données
- [ ] Tester l'upload de fichier (si fonctionnalité disponible)
- [ ] Vérifier que les modèles ML sont accessibles

---

## ⚠️ Points d'Attention

### Variables d'Environnement

Render injecte automatiquement:
- `DATABASE_URL` - Depuis PostgreSQL (format: `postgresql://user:pass@host:port/db`)
- `REDIS_URL` - Depuis Redis (format: `redis://:pass@host:port`)
- `PORT` - Port sur lequel écouter

**Important**: Ne pas définir `PORT` manuellement, Render le gère.

### Base de Données

- La première fois, les tables doivent être créées
- Le script `init_db.py` s'exécute automatiquement via l'entrypoint
- Vérifier les logs pour confirmer l'initialisation

### Redis

- Si Redis n'est pas créé, l'application utilisera SimpleCache
- C'est acceptable pour le développement, mais Redis est recommandé en production

### Sleep Mode (Plan Gratuit)

- Sur le plan gratuit, l'application peut s'endormir après 15 min d'inactivité
- Le premier accès après le sleep peut prendre 30-60 secondes
- Pour éviter cela, passer au plan Starter ($7/mois)

---

## 🐛 Dépannage Rapide

### Application ne démarre pas

1. Vérifier les logs dans Render
2. Vérifier que `SECRET_KEY` est défini
3. Vérifier que `DATABASE_URL` est présent (via Link Resource)

### Erreur de connexion à la base de données

1. Vérifier que PostgreSQL est démarré
2. Vérifier que les services sont liés
3. Vérifier `DATABASE_URL` dans les variables d'environnement

### Erreur Redis

1. Si Redis n'est pas critique, mettre `CACHE_TYPE=SimpleCache`
2. Sinon, vérifier que Redis est créé et lié

### Build échoue

1. Vérifier les logs de build
2. Vérifier que `requirements.txt` est correct
3. Vérifier que le Dockerfile est valide

---

## 📚 Documentation

- Guide complet: `GUIDE_DEPLOIEMENT_RENDER.md`
- Documentation Render: https://render.com/docs

---

**Statut**: ✅ **PRÊT POUR LE DÉPLOIEMENT**

