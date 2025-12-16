# 🚀 Guide de Déploiement en Production

Ce guide vous accompagne dans le déploiement de l'application BoursA en production.

## 📋 Prérequis

- Docker et Docker Compose installés
- Un serveur Linux (Ubuntu 20.04+ recommandé)
- Domaine configuré (pour HTTPS)
- Accès root ou sudo

## 🔧 Étapes de Déploiement

### 1. Préparation de l'environnement

#### Cloner le repository
```bash
git clone <votre-repository>
cd Projet-ML-Sea3/Projet-ML-Sea3
```

#### Créer le fichier `.env`
```bash
cp ENV_EXAMPLE.txt .env
nano .env  # ou votre éditeur préféré
```

**Variables OBLIGATOIRES à configurer :**
- `SECRET_KEY` : Générer avec `python -c "import secrets; print(secrets.token_hex(32))"`
- `REDIS_PASSWORD` : Mot de passe fort pour Redis
- `FLASK_ENV=production`

**Variables RECOMMANDÉES :**
- `CACHE_REDIS_URL` : URL complète Redis
- `DISABLE_PUBLIC_REGISTRATION=true` : Désactiver l'inscription publique

### 2. Configuration SSL/TLS

#### Option A : Let's Encrypt (Recommandé)

```bash
# Installer Certbot
sudo apt-get update
sudo apt-get install certbot

# Obtenir un certificat (remplacer votre-domaine.com)
sudo certbot certonly --standalone -d votre-domaine.com -d www.votre-domaine.com

# Créer le dossier pour les certificats
mkdir -p nginx/ssl

# Copier les certificats
sudo cp /etc/letsencrypt/live/votre-domaine.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/votre-domaine.com/privkey.pem nginx/ssl/key.pem
sudo chown $USER:$USER nginx/ssl/*.pem
```

#### Option B : Certificats auto-signés (Développement uniquement)

```bash
mkdir -p nginx/ssl
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem \
  -days 365 \
  -subj "/CN=votre-domaine.com"
```

⚠️ **Ne jamais utiliser de certificats auto-signés en production !**

### 3. Construction et Démarrage

#### Construire les images Docker
```bash
docker-compose -f docs/docker-compose.prod.yml build
```

#### Démarrer les services
```bash
docker-compose -f docs/docker-compose.prod.yml up -d
```

#### Vérifier le statut
```bash
docker-compose -f docs/docker-compose.prod.yml ps
docker-compose -f docs/docker-compose.prod.yml logs -f
```

### 4. Vérification

#### Tester l'endpoint de santé
```bash
curl http://localhost/health
# ou
curl https://votre-domaine.com/health
```

#### Vérifier les logs
```bash
# Logs de l'application
docker-compose -f docs/docker-compose.prod.yml logs flask_app_1

# Logs Nginx
docker-compose -f docs/docker-compose.prod.yml logs nginx

# Logs Redis
docker-compose -f docs/docker-compose.prod.yml logs redis
```

## 🔄 Mises à Jour

### Mettre à jour l'application

```bash
# Arrêter les services
docker-compose -f docs/docker-compose.prod.yml down

# Récupérer les dernières modifications
git pull

# Reconstruire les images
docker-compose -f docs/docker-compose.prod.yml build

# Redémarrer
docker-compose -f docs/docker-compose.prod.yml up -d
```

### Mettre à jour les certificats SSL

```bash
# Renouveler les certificats Let's Encrypt
sudo certbot renew

# Copier les nouveaux certificats
sudo cp /etc/letsencrypt/live/votre-domaine.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/votre-domaine.com/privkey.pem nginx/ssl/key.pem
sudo chown $USER:$USER nginx/ssl/*.pem

# Redémarrer Nginx
docker-compose -f docs/docker-compose.prod.yml restart nginx
```

## 🛠️ Maintenance

### Sauvegardes

#### Base de données
```bash
# Sauvegarder la base SQLite (si utilisée)
cp user_locations.db backups/user_locations_$(date +%Y%m%d).db

# Sauvegarder Redis
docker exec boursa_redis redis-cli --rdb /data/dump.rdb
```

#### Fichiers uploadés
```bash
tar -czf backups/uploads_$(date +%Y%m%d).tar.gz uploads/
```

### Monitoring

#### Vérifier l'utilisation des ressources
```bash
docker stats
```

#### Vérifier l'espace disque
```bash
df -h
docker system df
```

#### Nettoyer les images Docker inutilisées
```bash
docker system prune -a
```

## 🐛 Dépannage

### L'application ne démarre pas

1. **Vérifier les logs**
   ```bash
   docker-compose -f docs/docker-compose.prod.yml logs
   ```

2. **Vérifier les variables d'environnement**
   ```bash
   docker-compose -f docs/docker-compose.prod.yml config
   ```

3. **Vérifier que SECRET_KEY est défini**
   ```bash
   grep SECRET_KEY .env
   ```

### Redis ne se connecte pas

1. **Vérifier que Redis est démarré**
   ```bash
   docker-compose -f docs/docker-compose.prod.yml ps redis
   ```

2. **Tester la connexion Redis**
   ```bash
   docker exec -it boursa_redis redis-cli ping
   ```

3. **Vérifier le mot de passe**
   ```bash
   docker exec -it boursa_redis redis-cli -a $REDIS_PASSWORD ping
   ```

### Nginx ne démarre pas

1. **Vérifier la configuration**
   ```bash
   docker exec boursa_nginx nginx -t
   ```

2. **Vérifier les certificats SSL**
   ```bash
   ls -la nginx/ssl/
   ```

3. **Vérifier les logs**
   ```bash
   docker-compose -f docs/docker-compose.prod.yml logs nginx
   ```

### Erreur 502 Bad Gateway

- Vérifier que les instances Flask sont démarrées
- Vérifier les logs des applications Flask
- Vérifier la connectivité réseau entre Nginx et Flask

## 📊 Architecture de Production

```
Internet
   ↓
[Nginx - Port 80/443]
   ↓ (Load Balancing)
[Flask App 1] [Flask App 2] [Flask App 3]
   ↓
[Redis Cache]
   ↓
[SQLite/PostgreSQL Database]
```

## 🔒 Sécurité

### Checklist de Sécurité

- [ ] `SECRET_KEY` fort et unique généré
- [ ] `REDIS_PASSWORD` fort configuré
- [ ] `DISABLE_PUBLIC_REGISTRATION=true` en production
- [ ] HTTPS activé avec certificat valide
- [ ] Firewall configuré (ports 80, 443 uniquement)
- [ ] Logs activés et surveillés
- [ ] Backups configurés et testés
- [ ] Mises à jour de sécurité appliquées

### Configuration du Firewall

```bash
# UFW (Ubuntu)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# iptables
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -j DROP
```

## 📞 Support

Pour plus d'informations :
- Consulter `SECURITY.md` pour les détails de sécurité
- Consulter `ANALYSE_DEPLOIEMENT.md` pour l'analyse complète
- Vérifier les logs en cas de problème

---

**Version** : 1.0  
**Dernière mise à jour** : Décembre 2025

