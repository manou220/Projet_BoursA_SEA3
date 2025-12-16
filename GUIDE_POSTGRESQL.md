# 🐘 Guide PostgreSQL - Configuration avec Base Existante

## ✅ Votre Situation

- ✅ Vous utilisez **PostgreSQL**
- ✅ Votre base de données **contient déjà des informations**
- ✅ Vous voulez connecter le projet à cette base

---

## 📋 ÉTAPE 1 : Rassembler les Informations

Vous devez avoir ces informations de votre base PostgreSQL :

### Informations Requises

1. **Host (Serveur)** :
   - Local : `localhost` ou `127.0.0.1`
   - Distant : `192.168.x.x` ou `db.example.com`

2. **Port** :
   - Par défaut PostgreSQL : `5432`

3. **Nom de la base de données** :
   - Le nom de votre base existante

4. **Nom d'utilisateur** :
   - Votre utilisateur PostgreSQL

5. **Mot de passe** :
   - Le mot de passe de votre utilisateur

### 📝 Remplissez ce formulaire :

```
Host : _______________
Port : _______________ (généralement 5432)
Base de données : _______________
Utilisateur : _______________
Mot de passe : _______________
```

---

## 🔧 ÉTAPE 2 : Configurer le Fichier .env

### 2.1 Vérifier si .env existe

```bash
# Dans PowerShell
Test-Path .env
```

### 2.2 Créer le fichier .env

**Si le fichier n'existe pas** :
```bash
Copy-Item ENV_EXAMPLE.txt .env
```

### 2.3 Format DATABASE_URL pour PostgreSQL

```bash
DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE
```

### 2.4 Exemple Concret

**Exemple avec vos informations** :
```bash
# Si votre base est locale
DATABASE_URL=postgresql://boursa_user:mon_mot_de_passe@localhost:5432/boursa_db

# Si votre base est distante
DATABASE_URL=postgresql://boursa_user:mon_mot_de_passe@192.168.1.100:5432/boursa_db

# Si votre base utilise SSL
DATABASE_URL=postgresql://boursa_user:mon_mot_de_passe@db.example.com:5432/boursa_db?sslmode=require
```

---

## ✅ ÉTAPE 3 : Configuration Complète dans .env

Ouvrez votre fichier `.env` et ajoutez/modifiez ces lignes :

```bash
# ============================================
# BASE DE DONNÉES POSTGRESQL (OBLIGATOIRE)
# ============================================
# Remplacez par VOS informations réelles
DATABASE_URL=postgresql://VOTRE_USER:VOTRE_PASSWORD@VOTRE_HOST:5432/VOTRE_DATABASE
SQLALCHEMY_DATABASE_URI=postgresql://VOTRE_USER:VOTRE_PASSWORD@VOTRE_HOST:5432/VOTRE_DATABASE

# ============================================
# ENVIRONNEMENT
# ============================================
FLASK_ENV=production
APP_CONFIG=production

# ============================================
# SÉCURITÉ (OBLIGATOIRE)
# ============================================
# Générer avec: python scripts/generate_keys.py
SECRET_KEY=votre-cle-secrete-generee-ici

# ============================================
# REDIS (si utilisé)
# ============================================
REDIS_PASSWORD=votre-mot-de-passe-redis
```

**⚠️ REMPLACEZ** :
- `VOTRE_USER` → Votre nom d'utilisateur PostgreSQL
- `VOTRE_PASSWORD` → Votre mot de passe PostgreSQL
- `VOTRE_HOST` → Votre host (localhost, IP, ou domaine)
- `VOTRE_DATABASE` → Le nom de votre base de données

---

## ✅ ÉTAPE 4 : Générer les Clés Secrètes

### 4.1 Générer SECRET_KEY et autres clés

```bash
python scripts/generate_keys.py
```

**Résultat** :
```
SECRET_KEY=a508cab10273ddb45feaa0e9100d38e667146ca90b7a8360bb8767e5bf4e47e2
REDIS_PASSWORD=gB2oQLZqCMM2Hc53VBhQS-j2FAEPH74F-mMXMhq5chQ
POSTGRES_PASSWORD=bgYzG_eoZelOfjBTxtlYXiFtIY6r_TsRsJ2duRpCUEc
```

### 4.2 Copier dans .env

Copiez la ligne `SECRET_KEY=...` dans votre fichier `.env`

---

## ✅ ÉTAPE 5 : Installer psycopg2 (si nécessaire)

PostgreSQL nécessite le driver `psycopg2` :

```bash
pip install psycopg2-binary
```

**Vérification** :
```bash
python -c "import psycopg2; print('✅ psycopg2 installé')"
```

---

## ✅ ÉTAPE 6 : Tester la Connexion

### 6.1 Test Simple (vérifier la configuration)

```bash
python test_connection.py
```

**Résultat attendu** :
```
[OK] DATABASE_URL trouve
   Connexion a : localhost:5432/boursa_db
   Type : PostgreSQL
```

### 6.2 Test Réel (vérifier la connexion)

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
Database : boursa_db
User : boursa_user
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

## ⚠️ IMPORTANT : Base de Données avec Données Existantes

### Votre base contient déjà des données

**Options** :

#### Option A : Utiliser la Base Existante (Recommandé)

Si votre base contient déjà les tables nécessaires :
1. ✅ Vérifiez que les tables existent :
   - `users`
   - `data_files`
   - `test_history`
   - `user_locations`

2. ✅ Testez la connexion :
   ```bash
   python test_db_real.py
   ```

3. ✅ Si les tables existent, vous pouvez utiliser la base directement

#### Option B : Créer les Tables Manquantes

Si certaines tables manquent :

```bash
# Créer uniquement les tables manquantes
python scripts/init_db.py
```

**⚠️ ATTENTION** : Ce script utilise `db.create_all()` qui ne crée que les tables qui n'existent pas. Vos données existantes seront préservées.

---

## ✅ ÉTAPE 7 : Vérifier les Tables Requises

### 7.1 Liste des Tables Requises

Le projet nécessite ces tables :

1. **`users`** : Utilisateurs et authentification
2. **`data_files`** : Métadonnées des fichiers uploadés
3. **`test_history`** : Historique des tests statistiques
4. **`user_locations`** : Localisations pour la cartographie

### 7.2 Vérifier les Tables Existantes

Le script `test_db_real.py` affichera les tables existantes.

**Si des tables manquent** :
```bash
python scripts/init_db.py
```

---

## ✅ ÉTAPE 8 : Vérifier la Configuration Complète

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

## ✅ ÉTAPE 9 : Tester l'Application

### 9.1 Démarrer l'application

```bash
python app_main.py
```

**Ou avec Gunicorn** :
```bash
gunicorn -w 1 -b 0.0.0.0:5000 wsgi:app
```

### 9.2 Vérifier le health check

Ouvrez un navigateur :
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

### Erreur : "relation does not exist"

**Solution** : Les tables n'existent pas. Exécutez :
```bash
python scripts/init_db.py
```

### Erreur : "psycopg2 not installed"

**Solution** : `pip install psycopg2-binary`

---

## 📋 Checklist Finale

Avant de déployer :

- [ ] Fichier `.env` créé et configuré
- [ ] `DATABASE_URL` avec vos informations PostgreSQL
- [ ] `SECRET_KEY` généré et défini
- [ ] `FLASK_ENV=production` défini
- [ ] `psycopg2-binary` installé
- [ ] Connexion testée avec succès (`python test_db_real.py`)
- [ ] Tables vérifiées (ou créées si nécessaire)
- [ ] Health check fonctionne
- [ ] Application démarre sans erreur

---

## 🎯 Prochaines Étapes

Une fois la connexion testée :

1. ✅ Vérifiez que toutes les tables nécessaires existent
2. ✅ Testez l'application localement
3. ✅ Configurez les certificats SSL pour le déploiement
4. ✅ Déployez avec Docker (si utilisé)

---

*Guide spécifique pour PostgreSQL avec base de données existante*

