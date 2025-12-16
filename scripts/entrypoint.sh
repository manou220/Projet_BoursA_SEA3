#!/bin/bash
# Script d'entrypoint pour les conteneurs Flask
# Initialise la base de données avant de démarrer Gunicorn

set -e

echo "🚀 Démarrage de l'application BoursA..."

# Attendre que PostgreSQL soit prêt (si utilisé)
if [ -n "$DATABASE_URL" ] && [[ "$DATABASE_URL" == *"postgresql"* ]]; then
    echo "⏳ Attente de PostgreSQL..."
    until python -c "import psycopg2; psycopg2.connect('$DATABASE_URL')" 2>/dev/null; do
        echo "PostgreSQL n'est pas encore prêt, attente..."
        sleep 2
    done
    echo "✅ PostgreSQL est prêt"
fi

# Initialiser la base de données
echo "🔧 Initialisation de la base de données..."
python scripts/init_db.py || {
    echo "⚠️  Erreur lors de l'initialisation de la base de données"
    echo "   L'application va quand même démarrer, mais certaines fonctionnalités peuvent ne pas fonctionner"
}

# Démarrer Gunicorn
echo "🚀 Démarrage de Gunicorn..."
echo "📍 Port: ${PORT:-5000}"
echo "🌐 Écoute sur: 0.0.0.0:${PORT:-5000}"

# S'assurer que PORT est exporté pour que la commande CMD puisse l'utiliser
export PORT=${PORT:-5000}

# Exécuter la commande passée (qui devrait être la commande Gunicorn)
exec "$@"

