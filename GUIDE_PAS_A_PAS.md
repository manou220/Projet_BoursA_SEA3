# 🚀 Guide Pas à Pas - Configuration de la Base de Données

## 📋 Vue d'Ensemble

Ce guide vous accompagne étape par étape pour configurer votre base de données SQL avec le projet.

---

## ✅ ÉTAPE 1 : Identifier Votre Base de Données

### Question 1 : Quel type de base de données avez-vous créé ?

**A)** PostgreSQL  
**B)** MySQL/MariaDB  
**C)** Je ne sais pas / Je dois vérifier

👉 **Notez votre réponse** : _______________

### Si vous ne savez pas :

**Pour PostgreSQL** :
- Port par défaut : **5432**
- Interface souvent : pgAdmin ou psql

**Pour MySQL** :
- Port par défaut : **3306**
- Interface souvent : phpMyAdmin ou MySQL Workbench

---

## ✅ ÉTAPE 2 : Rassembler les Informations

Vous devez avoir ces informations :

### Informations Requises

1. **Host (Serveur)** :
   - Local : `localhost` ou `127.0.0.1`
   - Distant : `192.168.x.x` ou `db.example.com`

2. **Port** :
   - PostgreSQL : `5432` (par défaut)
   - MySQL : `3306` (par défaut)

3. **Nom de la base de données** :
   - Exemple : `boursa`, `boursa_db`, `ml_sea3`, etc.

4. **Nom d'utilisateur** :
   - Exemple : `boursa_user`, `root`, `admin`, etc.

5. **Mot de passe** :
   - Le mot de passe que vous avez défini

### 📝 Remplissez ce formulaire :

```
Host : _______________
Port : _______________
Base de données : _______________
Utilisateur : _______________
Mot de passe : _______________
```

---

## ✅ ÉTAPE 3 : Créer/Modifier le Fichier .env

### 3.1 Vérifier si .env existe

```bash
# Dans PowerShell
Test-Path .env
```

**Si `False`** → Le fichier n'existe pas, on va le créer  
**Si `True`** → Le fichier existe, on va le modifier

### 3.2 Créer le fichier .env

**Option A : Copier depuis ENV_EXAMPLE.txt**

```bash
# Dans PowerShell
Copy-Item ENV_EXAMPLE.txt .env
```

**Option B : Créer manuellement**

1. Créez un fichier nommé `.env` à la racine du projet
2. Ouvrez-le avec un éditeur de texte

---

## ✅ ÉTAPE 4 : Configurer DATABASE_URL

### 4.1 Format selon le type de base

**Si PostgreSQL** :
```bash
DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE
```

**Si MySQL** :
```bash
DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@HOST:PORT/DATABASE
```

### 4.2 Exemple Concret

**Exemple PostgreSQL local** :
```bash
DATABASE_URL=postgresql://boursa_user:mon_mot_de_passe@localhost:5432/boursa_db
```

**Exemple MySQL local** :
```bash
DATABASE_URL=mysql+pymysql://boursa_user:mon_mot_de_passe@localhost:3306/boursa_db
```

### 4.3 Ajouter dans .env

Ouvrez votre fichier `.env` et ajoutez/modifiez ces lignes :

```bash
# ============================================
# BASE DE DONNÉES (OBLIGATOIRE)
# ============================================
DATABASE_URL=postgresql://VOTRE_USER:VOTRE_PASSWORD@VOTRE_HOST:VOTRE_PORT/VOTRE_DATABASE
SQLALCHEMY_DATABASE_URI=postgresql://VOTRE_USER:VOTRE_PASSWORD@VOTRE_HOST:VOTRE_PORT/VOTRE_DATABASE

# ============================================
# ENVIRONNEMENT
# ============================================
FLASK_ENV=production
APP_CONFIG=production
```

**⚠️ REMPLACEZ** :
- `VOTRE_USER` → Votre nom d'utilisateur
- `VOTRE_PASSWORD` → Votre mot de passe
- `VOTRE_HOST` → Votre host (localhost, IP, ou domaine)
- `VOTRE_PORT` → Votre port (5432 pour PostgreSQL, 3306 pour MySQL)
- `VOTRE_DATABASE` → Le nom de votre base de données

---

## ✅ ÉTAPE 5 : Générer les Clés Secrètes

### 5.1 Générer SECRET_KEY

```bash
python scripts/generate_keys.py
```

**Ou manuellement** :
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
```

### 5.2 Copier les valeurs dans .env

Le script va afficher quelque chose comme :
```
SECRET_KEY=a508cab10273ddb45feaa0e9100d38e667146ca90b7a8360bb8767e5bf4e47e2
REDIS_PASSWORD=gB2oQLZqCMM2Hc53VBhQS-j2FAEPH74F-mMXMhq5chQ
POSTGRES_PASSWORD=bgYzG_eoZelOfjBTxtlYXiFtIY6r_TsRsJ2duRpCUEc
```

**Copiez ces lignes dans votre fichier `.env`**

---

## ✅ ÉTAPE 6 : Tester la Connexion

### 6.1 Créer un script de test

Créez un fichier `test_connection.py` :

```python
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv('DATABASE_URL')
if database_url:
    print(f"✅ DATABASE_URL trouvé")
    # Masquer le mot de passe
    if '@' in database_url:
        safe_url = database_url.split('@')[1]
        print(f"   Connexion à : {safe_url}")
    else:
        print(f"   Format : {database_url[:20]}...")
else:
    print("❌ DATABASE_URL non trouvé dans .env")
```

### 6.2 Exécuter le test

```bash
python test_connection.py
```

**Résultat attendu** : `✅ DATABASE_URL trouvé`

---

## ✅ ÉTAPE 7 : Tester la Connexion Réelle

### 7.1 Test PostgreSQL

```python
# test_db_real.py
import os
from dotenv import load_dotenv

load_dotenv()

try:
    import psycopg2
    from urllib.parse import urlparse
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL non configuré")
        exit(1)
    
    # Parser l'URL
    parsed = urlparse(database_url)
    
    # Connexion
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        database=parsed.path[1:],  # Enlever le premier /
        user=parsed.username,
        password=parsed.password
    )
    
    print("✅ Connexion à PostgreSQL réussie!")
    
    # Test simple
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"   Version PostgreSQL : {version[0][:50]}...")
    
    cursor.close()
    conn.close()
    
except ImportError:
    print("❌ psycopg2 non installé. Installez avec: pip install psycopg2-binary")
except Exception as e:
    print(f"❌ Erreur de connexion : {e}")
```

### 7.2 Test MySQL

```python
# test_db_real_mysql.py
import os
from dotenv import load_dotenv

load_dotenv()

try:
    import pymysql
    from urllib.parse import urlparse
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url or not database_url.startswith('mysql'):
        print("❌ DATABASE_URL MySQL non configuré")
        exit(1)
    
    # Parser l'URL (enlever mysql+pymysql://)
    url_clean = database_url.replace('mysql+pymysql://', 'mysql://')
    parsed = urlparse(url_clean)
    
    # Connexion
    conn = pymysql.connect(
        host=parsed.hostname,
        port=parsed.port or 3306,
        database=parsed.path[1:],
        user=parsed.username,
        password=parsed.password
    )
    
    print("✅ Connexion à MySQL réussie!")
    
    # Test simple
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION();")
    version = cursor.fetchone()
    print(f"   Version MySQL : {version[0]}")
    
    cursor.close()
    conn.close()
    
except ImportError:
    print("❌ pymysql non installé. Installez avec: pip install pymysql")
except Exception as e:
    print(f"❌ Erreur de connexion : {e}")
```

### 7.3 Exécuter le test approprié

**Pour PostgreSQL** :
```bash
python test_db_real.py
```

**Pour MySQL** :
```bash
python test_db_real_mysql.py
```

**Résultat attendu** : `✅ Connexion réussie!`

---

## ✅ ÉTAPE 8 : Initialiser les Tables

### 8.1 Installer les dépendances si nécessaire

**Pour PostgreSQL** :
```bash
pip install psycopg2-binary
```

**Pour MySQL** :
```bash
pip install pymysql
```

### 8.2 Créer les tables

```bash
python scripts/init_db.py
```

**Résultat attendu** :
```
🔧 Initialisation de la base de données...
📦 Création des tables...
✅ Tables créées avec succès
👤 Initialisation de la table utilisateurs...
✅ Table utilisateurs initialisée
📍 Vérification des localisations...
✅ X localisations trouvées
✅ Initialisation terminée avec succès!
```

---

## ✅ ÉTAPE 9 : Vérifier la Configuration Complète

### 9.1 Exécuter le script de vérification

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

## ✅ ÉTAPE 10 : Tester l'Application

### 10.1 Démarrer l'application

```bash
python app_main.py
```

**Ou avec Gunicorn** :
```bash
gunicorn -w 1 -b 0.0.0.0:5000 wsgi:app
```

### 10.2 Vérifier le health check

Ouvrez un navigateur ou utilisez curl :
```bash
curl http://localhost:5000/health
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

## 🎯 Checklist Finale

Avant de déployer, vérifiez :

- [ ] Fichier `.env` créé et configuré
- [ ] `DATABASE_URL` correctement formaté
- [ ] `SECRET_KEY` généré et défini
- [ ] `FLASK_ENV=production` défini
- [ ] Connexion à la base de données testée
- [ ] Tables créées avec succès
- [ ] Health check fonctionne
- [ ] Application démarre sans erreur

---

## 🆘 Problèmes Courants

### Erreur : "DATABASE_URL not set"

**Solution** : Vérifiez que `DATABASE_URL` est dans votre `.env`

### Erreur : "password authentication failed"

**Solution** : Vérifiez le mot de passe dans `DATABASE_URL`

### Erreur : "connection refused"

**Solution** : 
- Vérifiez que votre base de données est démarrée
- Vérifiez le host et le port
- Vérifiez les règles de firewall

### Erreur : "database does not exist"

**Solution** : Créez la base de données dans votre serveur SQL

### Erreur : "psycopg2 not installed"

**Solution** : `pip install psycopg2-binary`

### Erreur : "pymysql not installed"

**Solution** : `pip install pymysql`

---

## 📞 Besoin d'Aide ?

Si vous êtes bloqué à une étape, notez :
1. À quelle étape vous êtes
2. Le message d'erreur exact
3. Le type de base de données (PostgreSQL ou MySQL)

---

*Guide créé pour vous accompagner pas à pas*

