# 🔑 Configuration Rapide des Clés API Boursières

## 🚀 Méthode Rapide (Recommandée)

### Option 1 : Script Automatique (Non-Interactif)

```bash
# Configurer Alpha Vantage
python scripts/setup_api_keys.py --alphavantage VOTRE_CLE_ALPHA_VANTAGE

# Configurer IEX Cloud
python scripts/setup_api_keys.py --iex-cloud sk-VOTRE_CLE_IEX

# Configurer les deux en une fois
python scripts/setup_api_keys.py --alphavantage VOTRE_CLE_ALPHA --iex-cloud sk-VOTRE_CLE_IEX

# Vérifier la configuration
python scripts/setup_api_keys.py --show
```

### Option 2 : Script Interactif

```bash
python scripts/configure_api_keys.py
```

Suivez les instructions à l'écran.

---

## 📋 Obtenir les Clés API

### Alpha Vantage (Gratuit)

1. **Visitez** : https://www.alphavantage.co/support/#api-key
2. **Remplissez le formulaire** (nom, email)
3. **Cliquez sur** "GET FREE API KEY"
4. **Vérifiez votre email** et copiez la clé
5. **Format** : `DEMO1234567890ABC` (lettres majuscules et chiffres)

### IEX Cloud (Gratuit avec Plan Gratuit)

1. **Visitez** : https://iexcloud.io/console/login
2. **Créez un compte** (gratuit)
3. **Accédez à** : https://iexcloud.io/console/tokens
4. **Générez un token** :
   - `pk-xxxxx` pour développement (Publishable Token)
   - `sk-xxxxx` pour production (Secret Token)
5. **Copiez la clé**

---

## ✅ Exemple Complet

```bash
# 1. Obtenir les clés (voir ci-dessus)

# 2. Configurer Alpha Vantage
python scripts/setup_api_keys.py --alphavantage DEMO1234567890ABC

# 3. Configurer IEX Cloud
python scripts/setup_api_keys.py --iex-cloud sk-1234567890abcdef1234567890abcdef

# 4. Vérifier
python scripts/setup_api_keys.py --show
```

**Résultat attendu** :
```
✅ Alpha Vantage: DEMO123456...ABC
✅ IEX Cloud: sk-1234...cdef
✅ Yahoo Finance: Disponible (pas de clé requise)
```

---

## 🔧 Méthode Manuelle

Si vous préférez configurer manuellement :

1. **Ouvrir le fichier `.env`** (ou le créer depuis `ENV_EXAMPLE.txt`)

2. **Ajouter les lignes** :
```env
# Clés API Boursières
ALPHAVANTAGE_KEY=VOTRE_CLE_ALPHA_VANTAGE
IEX_CLOUD_API_KEY=sk-VOTRE_CLE_IEX_CLOUD
```

3. **Sauvegarder le fichier**

4. **Redémarrer l'application**

---

## ✅ Vérification

### Vérifier avec le Script

```bash
python scripts/setup_api_keys.py --show
```

### Vérifier avec le Script de Test

```bash
python scripts/check_stock_api_loading.py
```

### Tester dans l'Application

1. **Démarrer l'application** :
```bash
python app_main.py
```

2. **Tester l'endpoint** :
```bash
curl http://localhost:5000/upload/api_list
```

3. **Vérifier la réponse** :
```json
{
  "success": true,
  "apis": {
    "alpha_vantage": {
      "has_key": true,  // ✅ Doit être true
      ...
    },
    "iex_cloud": {
      "has_key": true,  // ✅ Doit être true
      ...
    }
  }
}
```

---

## 🆘 Dépannage

### Erreur : "Format invalide"

**Alpha Vantage** :
- ✅ Format correct : `DEMO1234567890ABC`
- ❌ Format incorrect : `demo-123` (minuscules et tirets)

**IEX Cloud** :
- ✅ Format correct : `sk-1234567890abcdef` ou `pk-1234567890abcdef`
- ❌ Format incorrect : `1234567890` (doit commencer par `sk-` ou `pk-`)

### Les clés ne sont pas chargées

1. Vérifiez que le fichier `.env` est dans le répertoire racine
2. Vérifiez que les noms des variables sont corrects :
   - `ALPHAVANTAGE_KEY` (pas `ALPHA_VANTAGE_KEY`)
   - `IEX_CLOUD_API_KEY` (pas `IEX_CLOUD_KEY`)
3. Redémarrez l'application

### Erreur : "Rate limit dépassé"

- **Alpha Vantage** : Attendez 1 minute (limite: 5 requêtes/min)
- **IEX Cloud** : Vérifiez votre quota dans la console
- **Yahoo Finance** : Attendez quelques secondes

---

## 📊 Statut des Plateformes

| Plateforme | Clé Requise | Statut Actuel |
|------------|-------------|---------------|
| **Yahoo Finance** | ❌ Non | ✅ Toujours disponible |
| **Alpha Vantage** | ✅ Oui | ⚠️ Configurez avec `--alphavantage` |
| **IEX Cloud** | ✅ Oui | ⚠️ Configurez avec `--iex-cloud` |

---

## 💡 Recommandations

- ✅ **Yahoo Finance** : Utilisez par défaut (pas de clé requise)
- ⚠️ **Alpha Vantage** : Utile pour données historiques détaillées
- ⚠️ **IEX Cloud** : Utile pour données en temps réel (meilleure fiabilité)

---

**Date** : Décembre 2025  
**Statut** : ✅ **PRÊT À UTILISER**

