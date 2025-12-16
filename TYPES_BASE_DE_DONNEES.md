# 🗄️ Types de Base de Données Utilisés dans le Projet

## 📊 Situation Actuelle

### Base de Données Par Défaut : **SQLite** ⚠️

**Statut actuel** : Le projet utilise **SQLite** comme base de données par défaut (fallback).

**Preuve** :
- ✅ Fichier `user_locations.db` existe dans le projet
- ✅ Code dans `app/__init__.py` utilise SQLite si `DATABASE_URL` n'est pas défini :
  ```python
  app.config.setdefault('SQLALCHEMY_DATABASE_URI', f"sqlite:///{app.config['DB_PATH']}")
  ```

**Utilisation SQLite** :
- ✅ **Développement** : SQLite est utilisé par défaut si aucune configuration n'est fournie
- ❌ **Production** : SQLite est **INTERDIT** et lève une exception

---

## 🎯 Base de Données Recommandée : **PostgreSQL**

### Pourquoi PostgreSQL ?

Le projet est **configuré pour PostgreSQL** en production car :

1. ✅ **Support de la concurrence** : Gère plusieurs instances Flask simultanées
2. ✅ **Performance** : Optimisé pour les applications multi-utilisateurs
3. ✅ **Architecture Docker** : Votre `docker-compose.prod.yml` utilise 3 instances Flask
4. ✅ **Pool de connexions** : Configuration déjà en place dans `app/config.py`

### Configuration PostgreSQL

**Format de connexion** :
```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
```

**Exemple** :
```bash
DATABASE_URL=postgresql://boursa_user:mon_mot_de_passe@localhost:5432/boursa_db
```

**Configuration dans le code** :
- `app/config.py` : Pool de connexions PostgreSQL configuré
- `app/__init__.py` : Utilise PostgreSQL si `DATABASE_URL` est défini
- `ProductionConfig` : **OBLIGE** PostgreSQL (lève une exception si SQLite)

---

## 🔄 Base de Données Alternative : **MySQL/MariaDB**

### Support MySQL

Le projet peut **aussi utiliser MySQL/MariaDB** si nécessaire.

**Format de connexion** :
```bash
DATABASE_URL=mysql+pymysql://username:password@host:port/database_name
```

**Exemple** :
```bash
DATABASE_URL=mysql+pymysql://boursa_user:mon_mot_de_passe@localhost:3306/boursa_db
```

**Dépendance requise** :
```bash
pip install pymysql
```

---

## 📋 Résumé des Types Supportés

| Type | Statut | Usage | Format DATABASE_URL |
|------|--------|-------|---------------------|
| **SQLite** | ⚠️ Par défaut (dev) | Développement uniquement | `sqlite:///path/to/db.db` |
| **PostgreSQL** | ✅ Recommandé | Production | `postgresql://user:pass@host:port/db` |
| **MySQL** | ✅ Supporté | Alternative | `mysql+pymysql://user:pass@host:port/db` |

---

## 🔍 Comment Vérifier Quel Type est Utilisé

### Méthode 1 : Vérifier le fichier `.env`

```bash
# Regarder la variable DATABASE_URL
type .env | findstr DATABASE_URL
```

**Si `DATABASE_URL` contient** :
- `postgresql://` → **PostgreSQL**
- `mysql+pymysql://` → **MySQL**
- `sqlite://` → **SQLite**
- **Absent** → **SQLite** (par défaut)

### Méthode 2 : Vérifier dans le code

```python
from app import create_app
app = create_app()
print(app.config['SQLALCHEMY_DATABASE_URI'])
```

### Méthode 3 : Script de vérification

```bash
python scripts/check_config.py
```

---

## 📊 Données Stockées

### Tables SQLAlchemy (tous types de bases)

1. **`users`** : Utilisateurs et authentification
2. **`data_files`** : Métadonnées des fichiers uploadés
3. **`test_history`** : Historique des tests statistiques
4. **`user_locations`** : Localisations pour la cartographie

### Fichier SQLite Direct (uniquement SQLite)

- **`user_locations.db`** : Fichier SQLite utilisé si PostgreSQL/MySQL non configuré

---

## ⚠️ Problème Actuel

### SQLite en Production = ❌ ERREUR

**Si vous déployez avec SQLite** :
- ❌ Erreur : `ValueError: DATABASE_URL avec PostgreSQL est OBLIGATOIRE en production`
- ❌ Conflits de verrous avec 3 instances Flask
- ❌ Erreurs `database is locked`

**Solution** : Configurer PostgreSQL ou MySQL dans `.env`

---

## ✅ Recommandation

### Pour le Déploiement

1. **Utilisez PostgreSQL** (recommandé) :
   ```bash
   DATABASE_URL=postgresql://user:password@host:5432/database
   ```

2. **OU utilisez MySQL** (alternative) :
   ```bash
   DATABASE_URL=mysql+pymysql://user:password@host:3306/database
   ```

3. **NE PAS utiliser SQLite** en production

### Pour le Développement

- SQLite est acceptable pour le développement local
- Mais PostgreSQL est recommandé même en dev pour tester la production

---

## 🔧 Migration depuis SQLite

Si vous avez des données dans SQLite et voulez migrer vers PostgreSQL :

```bash
# 1. Configurer DATABASE_URL avec PostgreSQL
# 2. Exécuter le script de migration
python scripts/migrate_to_postgresql.py
```

---

## 📝 Conclusion

**Type actuel** : SQLite (par défaut, développement)
**Type recommandé** : PostgreSQL (production)
**Type alternatif** : MySQL/MariaDB (si préféré)

**Action requise** : Configurer `DATABASE_URL` avec PostgreSQL ou MySQL dans votre fichier `.env` pour le déploiement.

---

*Document créé pour clarifier les types de bases de données supportés*

