# 🔑 Guide de Configuration des Clés API Boursières

## 📋 Vue d'Ensemble

Ce guide explique comment obtenir et configurer les clés API pour les plateformes boursières supportées par l'application.

---

## 🎯 Plateformes Supportées

### 1. Yahoo Finance ✅ (Toujours Disponible)

- ✅ **Gratuit** : Oui, pas de clé API requise
- ✅ **Quotas** : ~2000 requêtes/min (pas de limite stricte)
- ✅ **Configuration** : Aucune configuration nécessaire

**Statut** : Fonctionne immédiatement sans configuration.

---

### 2. Alpha Vantage ⚠️ (Nécessite une Clé)

- ⚠️ **Gratuit** : Oui, mais clé API requise
- ⚠️ **Quotas gratuits** : 5 requêtes/min, 500 requêtes/jour
- ⚠️ **Configuration** : Nécessite `ALPHAVANTAGE_KEY`

#### Comment Obtenir une Clé Alpha Vantage

1. **Visitez** : https://www.alphavantage.co/support/#api-key
2. **Remplissez le formulaire** :
   - Nom
   - Email
   - Organisation (optionnel)
3. **Cliquez sur** "GET FREE API KEY"
4. **Vérifiez votre email** : La clé sera envoyée par email
5. **Copiez la clé** : Format `XXXXXXXXXXXXXX` (lettres majuscules et chiffres)

#### Configuration

**Option 1 : Script automatique** (Recommandé)
```bash
python scripts/configure_api_keys.py
```

**Option 2 : Manuel**
```bash
# Ajouter dans .env
ALPHAVANTAGE_KEY=VOTRE_CLE_ICI
```

---

### 3. IEX Cloud ⚠️ (Nécessite une Clé)

- ⚠️ **Gratuit** : Oui avec plan gratuit, clé API requise
- ⚠️ **Quotas gratuits** : ~100 requêtes/min, ~50 000 requêtes/mois
- ⚠️ **Configuration** : Nécessite `IEX_CLOUD_API_KEY`

#### Comment Obtenir une Clé IEX Cloud

1. **Visitez** : https://iexcloud.io/console/login
2. **Créez un compte** : Inscription gratuite
3. **Accédez à la console** : https://iexcloud.io/console/tokens
4. **Générez un token** :
   - Choisissez "Publishable Token" (pk-) pour le développement
   - Ou "Secret Token" (sk-) pour la production
5. **Copiez la clé** : Format `sk-xxxxx` ou `pk-xxxxx`

#### Configuration

**Option 1 : Script automatique** (Recommandé)
```bash
python scripts/configure_api_keys.py
```

**Option 2 : Manuel**
```bash
# Ajouter dans .env
IEX_CLOUD_API_KEY=sk-votre_cle_ici
```

---

## 🚀 Configuration Rapide

### Méthode Automatique (Recommandée)

```bash
# Exécuter le script de configuration
python scripts/configure_api_keys.py
```

Le script vous guidera étape par étape pour :
- Configurer Alpha Vantage
- Configurer IEX Cloud
- Vérifier la configuration actuelle

### Méthode Manuelle

1. **Ouvrir le fichier `.env`** (ou le créer depuis `ENV_EXAMPLE.txt`)

2. **Ajouter les clés** :
```env
# Clés API Boursières
ALPHAVANTAGE_KEY=VOTRE_CLE_ALPHA_VANTAGE
IEX_CLOUD_API_KEY=sk-votre_cle_iex_cloud
```

3. **Sauvegarder le fichier**

4. **Redémarrer l'application** pour que les changements prennent effet

---

## ✅ Vérification de la Configuration

### Vérifier avec le Script

```bash
python scripts/check_stock_api_loading.py
```

### Vérifier Manuellement

```bash
# Vérifier que les variables sont chargées
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Alpha Vantage:', 'OK' if os.getenv('ALPHAVANTAGE_KEY') else 'NON CONFIGURE'); print('IEX Cloud:', 'OK' if os.getenv('IEX_CLOUD_API_KEY') else 'NON CONFIGURE')"
```

### Tester dans l'Application

1. **Démarrer l'application** :
```bash
python app_main.py
```

2. **Tester l'endpoint** :
```bash
# Lister les APIs disponibles
curl http://localhost:5000/upload/api_list
```

3. **Vérifier la réponse** :
```json
{
  "success": true,
  "apis": {
    "alpha_vantage": {
      "has_key": true,  // Doit être true si configuré
      ...
    },
    "iex_cloud": {
      "has_key": true,  // Doit être true si configuré
      ...
    }
  }
}
```

---

## 🔒 Sécurité

### ⚠️ Important

- **Ne commitez JAMAIS** le fichier `.env` dans Git
- **Ne partagez JAMAIS** vos clés API publiquement
- **Utilisez des clés différentes** pour développement et production

### Vérification Git

Assurez-vous que `.env` est dans `.gitignore` :

```bash
# Vérifier
cat .gitignore | grep -E "^\.env$"
```

Si `.env` n'est pas dans `.gitignore`, ajoutez-le :

```bash
echo ".env" >> .gitignore
```

---

## 📊 Comparaison des Plateformes

| Plateforme | Clé Requise | Quotas Gratuits | Intervalles | Recommandation |
|------------|-------------|-----------------|-------------|----------------|
| **Yahoo Finance** | ❌ Non | ~2000/min | 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo | ✅ **Par défaut** |
| **Alpha Vantage** | ✅ Oui | 5/min, 500/jour | daily, weekly, monthly | ⚠️ Pour données historiques |
| **IEX Cloud** | ✅ Oui | ~100/min, ~50k/mois | 1d, 1w, 1mo | ⚠️ Pour données en temps réel |

---

## 🆘 Dépannage

### Erreur : "Clé API Alpha Vantage manquante"

**Solution** :
1. Vérifiez que `ALPHAVANTAGE_KEY` est dans `.env`
2. Vérifiez le format (lettres majuscules et chiffres uniquement)
3. Redémarrez l'application

### Erreur : "Clé API IEX Cloud invalide"

**Solution** :
1. Vérifiez que `IEX_CLOUD_API_KEY` est dans `.env`
2. Vérifiez le format (doit commencer par `sk-` ou `pk-`)
3. Vérifiez que la clé n'a pas expiré dans la console IEX Cloud

### Erreur : "Rate limit dépassé"

**Solution** :
- **Alpha Vantage** : Attendez 1 minute (limite: 5 requêtes/min)
- **IEX Cloud** : Vérifiez votre quota dans la console
- **Yahoo Finance** : Attendez quelques secondes

### Les clés ne sont pas chargées

**Solution** :
1. Vérifiez que le fichier `.env` est dans le répertoire racine du projet
2. Vérifiez que `python-dotenv` est installé : `pip install python-dotenv`
3. Redémarrez l'application

---

## 📝 Exemple de Configuration Complète

```env
# ============================================
# CLES API BOURSIERES
# ============================================

# Alpha Vantage (gratuit)
# Obtenir sur: https://www.alphavantage.co/support/#api-key
ALPHAVANTAGE_KEY=DEMO1234567890ABC

# IEX Cloud (gratuit avec plan gratuit)
# Obtenir sur: https://iexcloud.io/console/tokens
IEX_CLOUD_API_KEY=sk-1234567890abcdef1234567890abcdef

# Yahoo Finance ne nécessite pas de clé
```

---

## 🎯 Recommandations

### Pour le Développement

- ✅ Utilisez **Yahoo Finance** par défaut (pas de clé requise)
- ⚠️ Configurez **Alpha Vantage** si vous avez besoin de données historiques détaillées

### Pour la Production

- ✅ Utilisez **Yahoo Finance** comme source principale
- ✅ Configurez **IEX Cloud** pour les données en temps réel (meilleure fiabilité)
- ⚠️ Utilisez **Alpha Vantage** comme fallback (quotas limités)

---

## ✅ Checklist de Configuration

- [ ] Clé Alpha Vantage obtenue (si nécessaire)
- [ ] Clé IEX Cloud obtenue (si nécessaire)
- [ ] Clés ajoutées dans `.env`
- [ ] `.env` ajouté à `.gitignore`
- [ ] Configuration vérifiée avec le script
- [ ] Application redémarrée
- [ ] Test de connexion réussi

---

**Date** : Décembre 2025  
**Statut** : ✅ **GUIDE COMPLET**

