# Guide de Configuration Sécurité et Performance

Ce document résume les améliorations de sécurité et performance implémentées dans l'application BoursA.

## 🎯 Fonctionnalités Implémentées

### ✅ 1. Authentification et Autorisation

- **Système d'authentification complet** avec Flask-Login
- **Gestion des rôles** : Admin, User, Viewer
- **Système de permissions** granulaire
- **Protection des routes** avec décorateurs
- **Verrouillage de compte** après tentatives échouées
- **Mots de passe hashés** avec werkzeug.security

#### Utilisation

```python
from app.auth.decorators import permission_required, admin_required
from app.models.user import Permission

@permission_required(Permission.UPLOAD)
def upload_file():
    # Route protégée par permission
    pass

@admin_required
def admin_panel():
    # Route réservée aux admins
    pass
```

#### Routes disponibles

- `/auth/login` - Connexion
- `/auth/logout` - Déconnexion
- `/auth/register` - Inscription (désactivable)
- `/auth/profile` - Profil utilisateur
- `/auth/users` - Liste des utilisateurs (admin uniquement)

#### Compte admin par défaut

À la première initialisation, un compte admin est créé :
- **Username** : `admin`
- **Password** : `admin123`

**⚠️ CHANGEZ LE MOT DE PASSE IMMÉDIATEMENT EN PRODUCTION !**

### ✅ 2. Cache Redis

- **Configuration Redis** pour améliorer les performances
- **Cache automatique** des données API boursières
- **Fallback vers SimpleCache** si Redis non disponible
- **Timeouts adaptés** selon le type de données

#### Installation Redis

```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# macOS
brew install redis
brew services start redis

# Docker
docker run -d -p 6379:6379 redis:alpine
```

#### Configuration

Ajoutez dans `.env` :
```env
CACHE_TYPE=Redis
CACHE_REDIS_URL=redis://localhost:6379/0
```

### ✅ 3. HTTPS/SSL

- **Configuration SSL/TLS** documentée
- **Headers de sécurité** configurés automatiquement
- **Support Let's Encrypt** pour certificats gratuits
- **Redirection HTTP → HTTPS** avec Nginx

Voir `docs/SECURITY.md` pour la configuration complète.

### ✅ 4. Load Balancing

- **Configuration Nginx** pour load balancing
- **Configuration HAProxy** alternative
- **Support multi-instances** de l'application
- **Docker Compose** pour déploiement complet

Voir `docs/nginx-ssl.conf.example` et `docs/docker-compose.prod.yml`.

## 📋 Checklist de Déploiement Production

### Sécurité

- [ ] Changer le mot de passe admin par défaut
- [ ] Générer une `SECRET_KEY` forte :
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- [ ] Définir `DISABLE_PUBLIC_REGISTRATION=true` dans `.env`
- [ ] Configurer HTTPS avec certificat valide (Let's Encrypt)
- [ ] Configurer le firewall (ports 80, 443 uniquement)
- [ ] Activer les logs et les surveiller

### Performance

- [ ] Installer et configurer Redis
- [ ] Configurer le load balancer (Nginx ou HAProxy)
- [ ] Démarrer plusieurs instances de l'application
- [ ] Activer la compression gzip
- [ ] Configurer le cache des assets statiques

### Variables d'Environnement Critiques

```env
# Sécurité
SECRET_KEY=<généré avec secrets.token_hex(32)>
FLASK_ENV=production
DISABLE_PUBLIC_REGISTRATION=true

# Cache
CACHE_TYPE=Redis
CACHE_REDIS_URL=redis://:password@localhost:6379/0

# APIs (optionnel)
ALPHAVANTAGE_KEY=your_key
IEX_CLOUD_API_KEY=your_key
```

## 🚀 Démarrage Rapide

### 1. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 2. Configuration

```bash
cp ENV_EXAMPLE.txt .env
# Éditez .env avec vos configurations
```

### 3. Initialisation de la base de données

```bash
python -c "from app import create_app; from app.models.user import init_users_table; app = create_app(); app.app_context().push(); init_users_table()"
```

### 4. Lancement

```bash
# Développement
python app_main.py

# Production avec Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

## 📚 Documentation Complémentaire

- `docs/SECURITY.md` - Guide complet de sécurité
- `docs/nginx-ssl.conf.example` - Configuration Nginx avec SSL
- `docs/docker-compose.prod.yml` - Déploiement Docker complet
- `app/services/README.md` - Documentation des APIs boursières

## 🔧 Dépannage

### Redis non disponible

L'application bascule automatiquement sur SimpleCache. Vérifiez :
- Redis est-il démarré ? `redis-cli ping` (doit répondre `PONG`)
- L'URL Redis est-elle correcte dans `.env` ?

### Erreurs d'authentification

- Vérifiez que la table `users` existe
- Vérifiez les logs : `logs/app.log`
- Réinitialisez le mot de passe admin si nécessaire

### HTTPS non fonctionnel

- Vérifiez que les certificats sont valides
- Vérifiez la configuration Nginx
- Vérifiez que le port 443 est ouvert

## 📞 Support

Pour toute question, consultez :
- La documentation Flask-Login : https://flask-login.readthedocs.io/
- La documentation Redis : https://redis.io/documentation
- La documentation Nginx : https://nginx.org/en/docs/

