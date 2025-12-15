# Guide Complet : Connexion aux APIs Boursières

Ce guide vous explique comment configurer et utiliser les APIs boursières dans votre application.

## 📋 Table des matières

1. [APIs Disponibles](#apis-disponibles)
2. [Configuration des Clés API](#configuration-des-clés-api)
3. [Utilisation du Service](#utilisation-du-service)
4. [Cache et Rate Limiting](#cache-et-rate-limiting)
5. [Exemples d'utilisation](#exemples-dutilisation)

---

## 🎯 APIs Disponibles

Votre application supporte **3 APIs boursières** :

### 1. Yahoo Finance ⭐ (Recommandé pour débuter)
- ✅ **Gratuit** : Pas de clé API requise
- 📊 **Quotas** : ~2000 requêtes/min (pas de limite stricte)
- ⏱️ **Intervalles** : `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo`
- 💾 **Cache** : 5 minutes
- 🔗 **Site** : https://finance.yahoo.com/

**Avantages** :
- Aucune configuration nécessaire
- Fonctionne immédiatement
- Supporte les actions, indices, crypto-monnaies

---

### 2. Alpha Vantage
- ✅ **Gratuit** : Clé API gratuite disponible
- 📊 **Quotas gratuits** : 5 requêtes/min, 500 requêtes/jour
- ⏱️ **Intervalles** : `daily`, `weekly`, `monthly`
- 💾 **Cache** : 1 heure (pour respecter les quotas)
- 🔗 **Site** : https://www.alphavantage.co/

**Avantages** :
- Données historiques complètes
- API stable et fiable
- Documentation excellente

**Inconvénients** :
- Quotas limités en version gratuite
- Nécessite une clé API

---

### 3. IEX Cloud
- ✅ **Gratuit** : Plan gratuit disponible
- 📊 **Quotas gratuits** : ~100 requêtes/min, ~50 000 requêtes/mois
- ⏱️ **Intervalles** : `1d`, `1w`, `1mo`
- 💾 **Cache** : 5 minutes
- 🔗 **Site** : https://iexcloud.io/

**Avantages** :
- Quotas généreux en version gratuite
- Données en temps réel
- API moderne et performante

**Inconvénients** :
- Nécessite une clé API
- Format de clé spécifique (`sk-xxx` ou `pk-xxx`)

---

## 🔑 Configuration des Clés API

### Étape 1 : Obtenir les Clés API

#### Alpha Vantage
1. Allez sur https://www.alphavantage.co/support/#api-key
2. Remplissez le formulaire (nom, email)
3. Vous recevrez votre clé API par email (format : `XXXXXXXXXXXXX`)
4. ⚠️ **Important** : La clé est gratuite mais limitée à 5 appels/min et 500/jour

#### IEX Cloud
1. Allez sur https://iexcloud.io/console/login
2. Créez un compte gratuit
3. Accédez à votre dashboard
4. Copiez votre clé API (format : `sk-xxxxx` ou `pk-xxxxx`)
5. ⚠️ **Important** : Vérifiez vos quotas dans le dashboard

### Étape 2 : Configurer les Variables d'Environnement

#### Option A : Fichier `.env` (Recommandé)

1. **Copiez le fichier d'exemple** :
   ```bash
   copy ENV_EXAMPLE.txt .env
   ```
   (Sur Linux/Mac : `cp ENV_EXAMPLE.txt .env`)

2. **Ouvrez le fichier `.env`** et ajoutez vos clés :
   ```env
   # Alpha Vantage
   ALPHAVANTAGE_KEY=VOTRE_CLE_ALPHA_VANTAGE_ICI
   
   # IEX Cloud
   IEX_CLOUD_API_KEY=sk-VOTRE_CLE_IEX_ICI
   ```

3. **Redémarrez l'application** pour que les changements prennent effet.

#### Option B : Variables d'Environnement Système

**Windows (PowerShell)** :
```powershell
$env:ALPHAVANTAGE_KEY="VOTRE_CLE_ICI"
$env:IEX_CLOUD_API_KEY="sk-VOTRE_CLE_ICI"
```

**Linux/Mac** :
```bash
export ALPHAVANTAGE_KEY="VOTRE_CLE_ICI"
export IEX_CLOUD_API_KEY="sk-VOTRE_CLE_ICI"
```

### Étape 3 : Vérifier la Configuration

1. **Démarrez votre application** :
   ```bash
   python app_main.py
   ```

2. **Testez l'endpoint de liste des APIs** :
   ```bash
   curl http://localhost:5000/upload/api_list
   ```
   
   Ou dans votre navigateur : `http://localhost:5000/upload/api_list`

3. **Vérifiez la réponse** :
   ```json
   {
     "success": true,
     "apis": {
       "yahoo": {
         "name": "Yahoo Finance",
         "requires_key": false,
         "has_key": true,
         "quotas": {...}
       },
       "alpha_vantage": {
         "name": "Alpha Vantage",
         "requires_key": true,
         "has_key": true,  // ← Doit être true si configuré
         "quotas": {...}
       },
       "iex_cloud": {
         "name": "IEX Cloud",
         "requires_key": true,
         "has_key": true,  // ← Doit être true si configuré
         "quotas": {...}
       }
     }
   }
   ```

---

## 🚀 Utilisation du Service

### Via l'Interface Web

L'application fournit une interface web pour récupérer des données :

1. **Accédez à la page d'upload** : `http://localhost:5000/upload`
2. **Sélectionnez "Récupérer depuis une API"**
3. **Choisissez l'API** : Yahoo Finance, Alpha Vantage ou IEX Cloud
4. **Entrez le symbole** : Ex. `AAPL`, `MSFT`, `BTC-USD`
5. **Sélectionnez l'intervalle** : Ex. `1d` pour quotidien
6. **Cliquez sur "Récupérer"**

Les données seront automatiquement chargées et disponibles pour l'analyse.

### Via l'API REST

#### Récupérer des Données

**Endpoint** : `POST /upload/api_fetch`

**Requête** :
```json
{
  "source": "yahoo",
  "symbol": "AAPL",
  "interval": "1d",
  "api_key": "optional_key_override"
}
```

**Réponse** :
```json
{
  "success": true,
  "filename": "yahoo_AAPL_1d.csv",
  "columns": ["Date", "Open", "High", "Low", "Close", "Volume"],
  "preview": [[...]],
  "dtypes": {...}
}
```

**Exemple avec cURL** :
```bash
curl -X POST http://localhost:5000/upload/api_fetch \
  -H "Content-Type: application/json" \
  -d '{
    "source": "yahoo",
    "symbol": "AAPL",
    "interval": "1d"
  }'
```

#### Lister les APIs Disponibles

**Endpoint** : `GET /upload/api_list`

**Réponse** :
```json
{
  "success": true,
  "apis": {
    "yahoo": {...},
    "alpha_vantage": {...},
    "iex_cloud": {...}
  }
}
```

### Via le Code Python

```python
from app.services.stock_api_service import get_stock_api_service, StockAPIError, RateLimitExceeded
from flask import current_app

# Obtenir le service (utilise le cache de l'application)
api_service = current_app.stock_api_service

# Récupérer des données depuis Yahoo Finance
try:
    df = api_service.fetch_stock_data(
        api_name='yahoo',
        symbol='AAPL',
        interval='1d'
    )
    print(df.head())
    
except RateLimitExceeded as e:
    print(f"Quota dépassé : {e}")
    # Attendre quelques minutes avant de réessayer
    
except StockAPIError as e:
    print(f"Erreur API : {e}")
    # Gérer l'erreur (symbole invalide, API indisponible, etc.)
```

---

## 💾 Cache et Rate Limiting

### Cache Intelligent

Le service implémente un **cache automatique** pour optimiser les performances :

- **Yahoo Finance** : Cache de 5 minutes
- **Alpha Vantage** : Cache de 1 heure (pour respecter les quotas)
- **IEX Cloud** : Cache de 5 minutes

**Avantages** :
- ✅ Réduit les appels API redondants
- ✅ Améliore les performances
- ✅ Respecte les quotas automatiquement
- ✅ Utilise Flask-Caching (SimpleCache en dev, Redis en prod)

**Comment ça marche** :
- Les données sont mises en cache automatiquement après chaque requête
- Les requêtes suivantes pour les mêmes paramètres utilisent le cache
- Le cache expire automatiquement selon le timeout configuré

### Rate Limiting

Le service gère automatiquement les **limites de requêtes** :

- **Yahoo Finance** : ~2000 requêtes/min
- **Alpha Vantage** : 5 requêtes/min, 500/jour
- **IEX Cloud** : ~100 requêtes/min

**Protection automatique** :
- ✅ Vérification avant chaque appel API
- ✅ Exception `RateLimitExceeded` si limite dépassée
- ✅ Messages d'erreur clairs

**Gestion des erreurs** :
```python
try:
    df = api_service.fetch_stock_data('alpha_vantage', 'AAPL', 'daily')
except RateLimitExceeded:
    # Attendre 60 secondes avant de réessayer
    time.sleep(60)
    df = api_service.fetch_stock_data('alpha_vantage', 'AAPL', 'daily')
```

---

## 📝 Exemples d'Utilisation

### Exemple 1 : Récupérer des Données Quotidiennes (Yahoo Finance)

```python
from app.services.stock_api_service import get_stock_api_service

api_service = get_stock_api_service()

# Récupérer les données d'Apple (AAPL) en quotidien
df = api_service.fetch_stock_data(
    api_name='yahoo',
    symbol='AAPL',
    interval='1d'
)

print(df.head())
# Output:
#         Date      Open      High       Low     Close    Volume
# 0 2024-01-01  185.50    186.20    184.80    185.90  50000000
# 1 2024-01-02  186.00    187.50    185.50    187.20  45000000
# ...
```

### Exemple 2 : Récupérer des Données Crypto (Yahoo Finance)

```python
# Bitcoin en USD
df_btc = api_service.fetch_stock_data(
    api_name='yahoo',
    symbol='BTC-USD',
    interval='1h'
)

# Ethereum en USD
df_eth = api_service.fetch_stock_data(
    api_name='yahoo',
    symbol='ETH-USD',
    interval='1d'
)
```

### Exemple 3 : Utiliser Alpha Vantage avec Gestion d'Erreurs

```python
from app.services.stock_api_service import StockAPIError, RateLimitExceeded
import time

try:
    df = api_service.fetch_stock_data(
        api_name='alpha_vantage',
        symbol='MSFT',
        interval='daily'
    )
    print(f"Récupéré {len(df)} lignes de données")
    
except RateLimitExceeded:
    print("Quota Alpha Vantage dépassé. Attente de 60 secondes...")
    time.sleep(60)
    # Réessayer
    df = api_service.fetch_stock_data(
        api_name='alpha_vantage',
        symbol='MSFT',
        interval='daily'
    )
    
except StockAPIError as e:
    print(f"Erreur API : {e}")
    # Essayer avec Yahoo Finance comme fallback
    df = api_service.fetch_stock_data(
        api_name='yahoo',
        symbol='MSFT',
        interval='1d'
    )
```

### Exemple 4 : Vérifier les APIs Disponibles

```python
apis = api_service.get_available_apis()

for api_name, api_info in apis.items():
    print(f"{api_info['name']}:")
    print(f"  - Clé requise: {api_info['requires_key']}")
    print(f"  - Clé configurée: {api_info['has_key']}")
    print(f"  - Quotas: {api_info['quotas']}")
    print()
```

---

## 🔧 Dépannage

### Problème : "Clé API manquante"

**Solution** :
1. Vérifiez que le fichier `.env` existe et contient la clé
2. Vérifiez le format de la clé (pas d'espaces, pas de guillemets)
3. Redémarrez l'application après modification du `.env`

### Problème : "Rate limit dépassé"

**Solution** :
1. Attendez quelques minutes avant de réessayer
2. Utilisez une autre API (Yahoo Finance n'a pas de limite stricte)
3. Vérifiez vos quotas sur le site de l'API
4. Le cache devrait réduire les appels redondants

### Problème : "Symbole invalide"

**Solution** :
1. Vérifiez le format du symbole (lettres, chiffres, tirets uniquement)
2. Pour les crypto-monnaies, utilisez `BTC-USD` et non `BTCUSD`
3. Vérifiez que le symbole existe sur l'API choisie

### Problème : "Timeout"

**Solution** :
1. Vérifiez votre connexion internet
2. L'API peut être temporairement indisponible
3. Réessayez après quelques secondes
4. Utilisez une autre API comme fallback

---

## 📚 Ressources

- **Documentation du service** : `app/services/README.md`
- **Code source** : `app/services/stock_api_service.py`
- **Exemple de configuration** : `ENV_EXAMPLE.txt`

---

## ✅ Checklist de Configuration

- [ ] Fichier `.env` créé à partir de `ENV_EXAMPLE.txt`
- [ ] Clé Alpha Vantage obtenue et ajoutée (optionnel)
- [ ] Clé IEX Cloud obtenue et ajoutée (optionnel)
- [ ] Application redémarrée après configuration
- [ ] Endpoint `/upload/api_list` testé et fonctionnel
- [ ] Test de récupération de données réussi

---

**🎉 Félicitations !** Votre application est maintenant configurée pour utiliser les APIs boursières réelles avec cache et rate limiting automatiques.

