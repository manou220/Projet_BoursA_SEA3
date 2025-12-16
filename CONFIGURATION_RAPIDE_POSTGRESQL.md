# 🚀 Configuration Rapide PostgreSQL

## ✅ Votre Situation

- ✅ Vous utilisez **PostgreSQL**
- ✅ Votre base contient **déjà des données**
- ✅ Vous voulez connecter le projet

---

## 📝 ÉTAPE 1 : Ouvrir le Fichier .env

1. Allez dans le répertoire du projet : `Projet-ML-Sea3/Projet-ML-Sea3/`
2. Si le fichier `.env` n'existe pas, copiez-le :
   ```bash
   Copy-Item ENV_EXAMPLE.txt .env
   ```
3. Ouvrez le fichier `.env` avec un éditeur de texte (Notepad++, VS Code, etc.)

---

## 📝 ÉTAPE 2 : Ajouter vos Informations PostgreSQL

Dans votre fichier `.env`, trouvez ou ajoutez ces lignes :

```bash
# ============================================
# BASE DE DONNÉES POSTGRESQL
# ============================================
DATABASE_URL=postgresql://VOTRE_USER:VOTRE_PASSWORD@VOTRE_HOST:VOTRE_PORT/VOTRE_DATABASE
SQLALCHEMY_DATABASE_URI=postgresql://VOTRE_USER:VOTRE_PASSWORD@VOTRE_HOST:VOTRE_PORT/VOTRE_DATABASE
```

### 🔧 Remplacez par VOS informations :

**Exemple si votre base est locale** :
```bash
DATABASE_URL=postgresql://postgres:mon_mot_de_passe@localhost:5432/ma_base
SQLALCHEMY_DATABASE_URI=postgresql://postgres:mon_mot_de_passe@localhost:5432/ma_base
```

**Exemple si votre base est distante** :
```bash
DATABASE_URL=postgresql://boursa_user:mon_mot_de_passe@192.168.1.100:5432/boursa_db
SQLALCHEMY_DATABASE_URI=postgresql://boursa_user:mon_mot_de_passe@192.168.1.100:5432/boursa_db
```

### 📋 Format de l'URL :

```
postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

**Où** :
- `USER` = Votre nom d'utilisateur PostgreSQL
- `PASSWORD` = Votre mot de passe PostgreSQL
- `HOST` = `localhost` (si local) ou l'IP/domaine de votre serveur
- `PORT` = `5432` (port par défaut PostgreSQL)
- `DATABASE` = Le nom de votre base de données

---

## 📝 ÉTAPE 3 : Configurer l'Environnement

Dans le même fichier `.env`, assurez-vous d'avoir :

```bash
FLASK_ENV=production
APP_CONFIG=production
```

---

## 📝 ÉTAPE 4 : Générer SECRET_KEY

Exécutez cette commande :

```bash
python scripts/generate_keys.py
```

**Résultat** :
```
SECRET_KEY=a508cab10273ddb45feaa0e9100d38e667146ca90b7a8360bb8767e5bf4e47e2
REDIS_PASSWORD=gB2oQLZqCMM2Hc53VBhQS-j2FAEPH74F-mMXMhq5chQ
POSTGRES_PASSWORD=bgYzG_eoZelOfjBTxtlYXiFtIY6r_TsRsJ2duRpCUEc
```

**Copiez la ligne `SECRET_KEY=...` dans votre fichier `.env`**

---

## ✅ ÉTAPE 5 : Tester la Configuration

### 5.1 Test Simple

```bash
python test_connection.py
```

**Résultat attendu** :
```
[OK] DATABASE_URL trouve
   Connexion a : localhost:5432/votre_base
   Type : PostgreSQL
```

### 5.2 Test Réel de Connexion

```bash
python test_db_real.py
```

**Résultat attendu** :
```
======================================================================
TEST DE CONNEXION POSTGRESQL
======================================================================
Host : localhost
Port : 5432
Database : votre_base
User : votre_user
----------------------------------------------------------------------
Tentative de connexion...
[OK] Connexion a PostgreSQL reussie!
[OK] Version PostgreSQL : PostgreSQL 15.x...
[OK] X table(s) trouvee(s) :
   - users
   - data_files
   ...
======================================================================
[OK] TEST REUSSI - La connexion fonctionne!
======================================================================
```

---

## ⚠️ IMPORTANT : Base avec Données Existantes

### Si votre base contient déjà des tables

Le script `test_db_real.py` affichera les tables existantes.

**Tables requises par le projet** :
- `users`
- `data_files`
- `test_history`
- `user_locations`

### Si des tables manquent

Exécutez :
```bash
python scripts/init_db.py
```

**⚠️ Ce script ne supprime PAS vos données existantes**, il crée uniquement les tables manquantes.

---

## ✅ ÉTAPE 6 : Vérifier la Configuration Complète

```bash
python scripts/check_config.py
```

**Résultat attendu** :
```
[OK] Fichier .env existe
[OK] DATABASE_URL: Configuré
[OK] SECRET_KEY: Configuré
[OK] FLASK_ENV: production
```

---

## ✅ ÉTAPE 7 : Tester l'Application

```bash
python app_main.py
```

Puis ouvrez dans votre navigateur :
```
http://localhost:5000/health
```

**Résultat attendu** :
```json
{
  "status": "healthy",
  "service": "boursa",
  "version": "1.0.0",
  "cache": "ok",
  "database": "ok"
}
```

---

## 🆘 Problèmes Courants

### Erreur : "password authentication failed"

**Solution** : Vérifiez le mot de passe dans `DATABASE_URL`

### Erreur : "connection refused"

**Solution** : 
- Vérifiez que PostgreSQL est démarré
- Vérifiez le host et le port
- Vérifiez les règles de firewall

### Erreur : "database does not exist"

**Solution** : Vérifiez le nom de la base de données dans `DATABASE_URL`

### Erreur : "psycopg2 not installed"

**Solution** : `pip install psycopg2-binary`

---

## 📋 Checklist

- [ ] Fichier `.env` créé/modifié
- [ ] `DATABASE_URL` configuré avec vos informations PostgreSQL
- [ ] `SECRET_KEY` généré et ajouté
- [ ] `FLASK_ENV=production` défini
- [ ] Test de connexion réussi (`python test_db_real.py`)
- [ ] Tables vérifiées (ou créées si nécessaire)
- [ ] Application démarre sans erreur

---

## 🎯 Exemple Complet de .env

Voici un exemple complet de fichier `.env` :

```bash
# ============================================
# BASE DE DONNÉES POSTGRESQL
# ============================================
DATABASE_URL=postgresql://postgres:mon_mot_de_passe@localhost:5432/ma_base
SQLALCHEMY_DATABASE_URI=postgresql://postgres:mon_mot_de_passe@localhost:5432/ma_base

# ============================================
# ENVIRONNEMENT
# ============================================
FLASK_ENV=production
APP_CONFIG=production

# ============================================
# SÉCURITÉ
# ============================================
SECRET_KEY=a508cab10273ddb45feaa0e9100d38e667146ca90b7a8360bb8767e5bf4e47e2

# ============================================
# REDIS (si utilisé)
# ============================================
REDIS_PASSWORD=votre-mot-de-passe-redis
```

**⚠️ REMPLACEZ** toutes les valeurs par vos informations réelles !

---

*Guide rapide pour configurer PostgreSQL*

