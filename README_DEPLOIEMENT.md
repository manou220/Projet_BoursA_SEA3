# 🚀 Guide de Déploiement - Vue d'Ensemble

## 📍 Répertoire de Travail

Toutes les commandes doivent être exécutées depuis :
```
D:\emman\Desktop\Projet-ML-Sea3\Projet-ML-Sea3
```

## ⚡ Déploiement Rapide (3 Commandes)

### 1. Générer le fichier .env

```powershell
# Windows PowerShell
.\scripts\generate_env.ps1

# Ou Linux/Mac
python scripts/generate_env.py
```

### 2. Déployer

```powershell
# Construire et démarrer
docker-compose -f docs/docker-compose.prod.yml build
docker-compose -f docs/docker-compose.prod.yml up -d
```

### 3. Vérifier

```powershell
# Vérifier le statut
docker-compose -f docs/docker-compose.prod.yml ps

# Tester la santé
Invoke-WebRequest http://localhost/health
```

## 📚 Documentation Disponible

1. **DEPLOIEMENT_WINDOWS.md** - Guide spécifique Windows
2. **COMMANDES_DEPLOIEMENT.md** - Commandes détaillées
3. **DEPLOIEMENT_INSTRUCTIONS.md** - Instructions complètes
4. **GUIDE_DEPLOIEMENT_RAPIDE.md** - Guide rapide
5. **docs/DEPLOIEMENT.md** - Guide de déploiement complet

## 🎯 Valeurs Générées pour Vous

Si vous avez besoin de générer manuellement les valeurs :

```powershell
# SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# REDIS_PASSWORD  
python -c "import secrets; print(secrets.token_urlsafe(24))"

# POSTGRES_PASSWORD
python -c "import secrets; print(secrets.token_urlsafe(24))"
```

## ✅ Checklist Rapide

- [ ] `.env` créé avec toutes les valeurs
- [ ] Docker Desktop démarré
- [ ] Services démarrés
- [ ] Health check OK
- [ ] Application accessible

## 🆘 Besoin d'Aide ?

1. Consultez les logs : `docker-compose -f docs/docker-compose.prod.yml logs`
2. Vérifiez le statut : `docker-compose -f docs/docker-compose.prod.yml ps`
3. Consultez la documentation dans `docs/`

---

**Prêt à déployer ?** Suivez `DEPLOIEMENT_WINDOWS.md` pour Windows ou `GUIDE_DEPLOIEMENT_RAPIDE.md` pour Linux/Mac.

