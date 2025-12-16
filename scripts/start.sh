#!/bin/bash
# Script de démarrage pour Render
# Utilise le PORT fourni par Render ou 5000 par défaut

set -e

# Récupérer le port depuis l'environnement (Render le définit automatiquement)
PORT=${PORT:-5000}

echo "🚀 Démarrage de l'application BoursA..."
echo "📍 Port: $PORT"
echo "🌐 Écoute sur: 0.0.0.0:$PORT"

# Démarrer Gunicorn
# Utiliser exec pour que Gunicorn soit le processus principal (PID 1)
# Important pour que Render détecte correctement le processus
exec gunicorn \
    -w 4 \
    -b 0.0.0.0:$PORT \
    --access-logfile - \
    --error-logfile - \
    --timeout 120 \
    --keep-alive 5 \
    wsgi:app

