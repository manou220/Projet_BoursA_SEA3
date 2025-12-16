# 📋 Étapes de Configuration des Clés API - Guide Complet

## 🎯 Objectif

Configurer les clés API pour Alpha Vantage et IEX Cloud afin d'utiliser toutes les plateformes boursières disponibles.

---

## 📝 ÉTAPE 1 : Obtenir la Clé API Alpha Vantage

### 1.1 Accéder au Site

1. **Ouvrez votre navigateur** et allez sur :
   ```
   https://www.alphavantage.co/support/#api-key
   ```

### 1.2 Remplir le Formulaire

2. **Remplissez les champs** :
   - **First Name** : Votre prénom
   - **Last Name** : Votre nom
   - **Email** : Votre adresse email
   - **Organization** : (Optionnel) Votre organisation

3. **Cliquez sur** "GET FREE API KEY"

### 1.3 Recevoir la Clé

4. **Vérifiez votre email** : Alpha Vantage vous enverra un email avec votre clé API
5. **Copiez la clé** : Format `DEMO1234567890ABC` (lettres majuscules et chiffres)

### 1.4 Exemple de Clé

```
DEMO1234567890ABC
```

**Note** : Les clés de démonstration commencent souvent par `DEMO`. Les clés réelles sont similaires mais uniques.

---

## 📝 ÉTAPE 2 : Obtenir la Clé API IEX Cloud

### 2.1 Créer un Compte

1. **Ouvrez votre navigateur** et allez sur :
   ```
   https://iexcloud.io/console/login
   ```

2. **Cliquez sur** "Sign Up" ou "Create Account"

3. **Remplissez le formulaire d'inscription** :
   - Email
   - Mot de passe
   - Confirmez votre email

### 2.2 Accéder aux Tokens

4. **Connectez-vous** avec vos identifiants

5. **Accédez à la page des tokens** :
   ```
   https://iexcloud.io/console/tokens
   ```

### 2.3 Générer un Token

6. **Choisissez le type de token** :
   - **Publishable Token** (`pk-xxxxx`) : Pour développement (peut être exposé publiquement)
   - **Secret Token** (`sk-xxxxx`) : Pour production (à garder secret)

7. **Générez le token** : Cliquez sur "Generate Token"

8. **Copiez la clé** : Format `sk-1234567890abcdef` ou `pk-1234567890abcdef`

### 2.4 Exemple de Clé

```
sk-1234567890abcdef1234567890abcdef
```

**Note** : Les clés commencent toujours par `sk-` (secret) ou `pk-` (publishable).

---

## 📝 ÉTAPE 3 : Configurer les Clés avec le Script

### 3.1 Ouvrir un Terminal

1. **Ouvrez PowerShell** ou **Invite de commandes**

2. **Naviguez vers le répertoire du projet** :
   ```powershell
   cd "D:\emman\Desktop\Projet-ML-Sea3\Projet-ML-Sea3\Projet-ML-Sea3"
   ```

### 3.2 Exécuter le Script de Configuration

3. **Remplacez `VOTRE_CLE_ALPHA` et `VOTRE_CLE_IEX`** par vos vraies clés :

```powershell
python scripts\setup_api_keys.py --alphavantage VOTRE_CLE_ALPHA --iex-cloud sk-VOTRE_CLE_IEX
```

**Exemple avec des clés fictives** :
```powershell
python scripts\setup_api_keys.py --alphavantage DEMO1234567890ABC --iex-cloud sk-1234567890abcdef1234567890abcdef
```

### 3.3 Résultat Attendu

Si tout fonctionne, vous devriez voir :
```
✅ Clé Alpha Vantage configurée avec succès!
✅ Clé IEX Cloud configurée avec succès!

======================================================================
✅ Configuration terminée!
======================================================================

💡 Note: Redémarrez l'application pour que les changements prennent effet.

======================================================================
CONFIGURATION ACTUELLE
======================================================================
✅ Alpha Vantage: DEMO123456...ABC
✅ IEX Cloud: sk-1234...cdef
✅ Yahoo Finance: Disponible (pas de clé requise)
```

---

## 📝 ÉTAPE 4 : Vérifier la Configuration

### 4.1 Vérifier avec le Script

```powershell
python scripts\setup_api_keys.py --show
```

**Résultat attendu** :
```
======================================================================
CONFIGURATION ACTUELLE
======================================================================
✅ Alpha Vantage: DEMO123456...ABC
✅ IEX Cloud: sk-1234...cdef
✅ Yahoo Finance: Disponible (pas de clé requise)
```

### 4.2 Vérifier avec le Script de Test Complet

```powershell
python scripts\check_stock_api_loading.py
```

**Résultat attendu** :
```
[OK] Yahoo Finance: Pas de cle API requise (toujours disponible)
[OK] Alpha Vantage: Cle API configuree (XX caracteres)
[OK] IEX Cloud: Cle API configuree (XX caracteres)
```

---

## 📝 ÉTAPE 5 : Redémarrer l'Application

### 5.1 Arrêter l'Application (si elle tourne)

1. **Si l'application tourne** : Appuyez sur `Ctrl+C` dans le terminal où elle tourne

### 5.2 Redémarrer l'Application

2. **Démarrer l'application** :
```powershell
python app_main.py
```

**Ou avec Gunicorn** :
```powershell
gunicorn -w 1 -b 0.0.0.0:5000 wsgi:app
```

### 5.3 Vérifier que les Clés sont Chargées

3. **Tester l'endpoint** (dans un autre terminal) :
```powershell
curl http://localhost:5000/upload/api_list
```

**Ou ouvrez dans votre navigateur** :
```
http://localhost:5000/upload/api_list
```

**Résultat attendu** :
```json
{
  "success": true,
  "apis": {
    "yahoo": {
      "name": "Yahoo Finance",
      "requires_key": false,
      "has_key": true,
      ...
    },
    "alpha_vantage": {
      "name": "Alpha Vantage",
      "requires_key": true,
      "has_key": true,  // ✅ Doit être true
      ...
    },
    "iex_cloud": {
      "name": "IEX Cloud",
      "requires_key": true,
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
- ✅ Correct : `DEMO1234567890ABC` (majuscules et chiffres)
- ❌ Incorrect : `demo-123` (minuscules ou caractères spéciaux)

**IEX Cloud** :
- ✅ Correct : `sk-1234567890abcdef` ou `pk-1234567890abcdef`
- ❌ Incorrect : `1234567890` (doit commencer par `sk-` ou `pk-`)

### Les clés ne sont pas chargées

1. **Vérifiez le fichier `.env`** :
   ```powershell
   # Vérifier que les clés sont présentes
   Get-Content .env | Select-String "ALPHAVANTAGE_KEY|IEX_CLOUD_API_KEY"
   ```

2. **Vérifiez les noms des variables** :
   - `ALPHAVANTAGE_KEY` (pas `ALPHA_VANTAGE_KEY`)
   - `IEX_CLOUD_API_KEY` (pas `IEX_CLOUD_KEY`)

3. **Redémarrez l'application**

### Erreur : "Rate limit dépassé"

- **Alpha Vantage** : Attendez 1 minute (limite: 5 requêtes/min)
- **IEX Cloud** : Vérifiez votre quota dans la console
- **Yahoo Finance** : Attendez quelques secondes

---

## ✅ Checklist Finale

- [ ] Clé Alpha Vantage obtenue
- [ ] Clé IEX Cloud obtenue
- [ ] Clés configurées avec le script
- [ ] Configuration vérifiée avec `--show`
- [ ] Application redémarrée
- [ ] Test de l'endpoint `/upload/api_list` réussi
- [ ] `has_key: true` pour Alpha Vantage et IEX Cloud

---

## 📊 Résumé des Commandes

```powershell
# 1. Configurer les clés
python scripts\setup_api_keys.py --alphavantage VOTRE_CLE_ALPHA --iex-cloud sk-VOTRE_CLE_IEX

# 2. Vérifier la configuration
python scripts\setup_api_keys.py --show

# 3. Vérifier avec le test complet
python scripts\check_stock_api_loading.py

# 4. Redémarrer l'application
python app_main.py

# 5. Tester l'endpoint
curl http://localhost:5000/upload/api_list
```

---

**Date** : Décembre 2025  
**Statut** : ✅ **GUIDE COMPLET**

