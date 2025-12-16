# 🔧 Fix: Render Port Detection Issue

## Problème

Render affiche: `No open HTTP ports detected on 0.0.0.0`

Cela signifie que Render ne détecte pas que l'application écoute sur un port HTTP.

## Solution Appliquée

### 1. Dockerfile Modifié

- ✅ Utilisation de `exec` dans la commande CMD pour que Gunicorn soit le processus principal
- ✅ La commande utilise `${PORT:-5000}` pour utiliser le PORT de Render ou 5000 par défaut
- ✅ Gunicorn écoute sur `0.0.0.0:${PORT}` (important pour Render)

### 2. Entrypoint Modifié

- ✅ Export explicite de la variable PORT
- ✅ Logs pour déboguer le port utilisé

## Vérifications dans Render

### 1. Variables d'Environnement

Assurez-vous que dans Render, vous n'avez **PAS** défini manuellement `PORT`. Render le définit automatiquement.

### 2. Configuration du Service

Dans Render, vérifiez:
- **Runtime**: Docker
- **Dockerfile Path**: `./Dockerfile` (ou laisser vide si à la racine)
- **Docker Context**: `.` (ou laisser vide)

### 3. Start Command

Dans Render, laissez le **Start Command** vide. Le Dockerfile gère tout via CMD.

## Alternative: Utiliser render.yaml

Si vous utilisez `render.yaml`, assurez-vous qu'il ne définit pas de PORT:

```yaml
services:
  - type: web
    name: boursa-app
    runtime: docker
    dockerfilePath: ./Dockerfile
    dockerContext: .
    # Ne PAS définir PORT ici, Render le gère automatiquement
    envVars:
      - key: FLASK_ENV
        value: production
```

## Test Local

Pour tester localement avec un port différent:

```bash
PORT=8080 docker run -p 8080:8080 -e PORT=8080 votre-image
```

L'application devrait écouter sur le port 8080.

## Vérification Post-Déploiement

Après le déploiement, vérifiez les logs Render:

1. Cherchez: `📍 Port: XXXX`
2. Cherchez: `🌐 Écoute sur: 0.0.0.0:XXXX`
3. Vérifiez que Gunicorn démarre correctement

Si vous voyez toujours l'erreur:

1. Vérifiez que le build a réussi
2. Vérifiez les logs pour voir sur quel port Gunicorn écoute
3. Assurez-vous que `PORT` n'est pas défini manuellement dans Render

## Solution Alternative (Si le problème persiste)

Si le problème persiste, vous pouvez créer un script de démarrage:

**Créer `scripts/start.sh`:**
```bash
#!/bin/bash
set -e

PORT=${PORT:-5000}
echo "Starting on port $PORT"

exec gunicorn -w 4 -b 0.0.0.0:$PORT --access-logfile - --error-logfile - wsgi:app
```

**Modifier Dockerfile:**
```dockerfile
COPY scripts/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
```

Mais normalement, la solution actuelle devrait fonctionner.

