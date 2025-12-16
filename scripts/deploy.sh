#!/bin/bash
# Script de déploiement automatisé pour BoursA
# Usage: ./scripts/deploy.sh [production|development]

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier l'environnement
ENV=${1:-production}
info "Déploiement en mode: $ENV"

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    error "Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    error "Docker Compose n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier que le fichier .env existe
if [ ! -f .env ]; then
    error "Le fichier .env n'existe pas. Créez-le à partir de ENV_EXAMPLE.txt"
    exit 1
fi

# Charger les variables d'environnement
export $(grep -v '^#' .env | xargs)

# Vérifier les variables obligatoires
if [ -z "$SECRET_KEY" ]; then
    error "SECRET_KEY n'est pas défini dans .env"
    exit 1
fi

if [ -z "$POSTGRES_PASSWORD" ]; then
    error "POSTGRES_PASSWORD n'est pas défini dans .env"
    exit 1
fi

# Créer les répertoires nécessaires
info "Création des répertoires nécessaires..."
mkdir -p uploads logs logs/nginx nginx/ssl app/models

# Générer les certificats SSL auto-signés si nécessaire (pour développement)
if [ ! -f nginx/ssl/cert.pem ] || [ ! -f nginx/ssl/key.pem ]; then
    warn "Certificats SSL non trouvés. Génération de certificats auto-signés..."
    mkdir -p nginx/ssl
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout nginx/ssl/key.pem \
        -out nginx/ssl/cert.pem \
        -subj "/C=FR/ST=State/L=City/O=BoursA/CN=localhost" 2>/dev/null || {
        warn "Impossible de générer les certificats SSL. Continuez sans HTTPS ou configurez-les manuellement."
    }
fi

# Arrêter les conteneurs existants
info "Arrêt des conteneurs existants..."
docker-compose down 2>/dev/null || docker compose down 2>/dev/null || true

# Construire les images
info "Construction des images Docker..."
docker-compose build || docker compose build

# Démarrer les services
info "Démarrage des services..."
if [ "$ENV" = "production" ]; then
    # Production: démarrer tous les services
    docker-compose up -d || docker compose up -d
else
    # Développement: démarrer sans nginx
    docker-compose up -d postgres redis flask_app || docker compose up -d postgres redis flask_app
fi

# Attendre que les services soient prêts
info "Attente du démarrage des services..."
sleep 10

# Vérifier la santé des services
info "Vérification de la santé des services..."

# Vérifier PostgreSQL
if docker exec boursa_postgres pg_isready -U ${POSTGRES_USER:-boursa_user} &> /dev/null; then
    info "✅ PostgreSQL est prêt"
else
    error "❌ PostgreSQL n'est pas prêt"
    exit 1
fi

# Vérifier Redis
if docker exec boursa_redis redis-cli ping &> /dev/null; then
    info "✅ Redis est prêt"
else
    warn "⚠️  Redis n'est pas accessible (peut être normal si un mot de passe est requis)"
fi

# Vérifier l'application Flask
sleep 5
if curl -f http://localhost:${APP_PORT:-5000}/health &> /dev/null; then
    info "✅ L'application Flask est prête"
else
    warn "⚠️  L'application Flask n'est pas encore prête. Vérifiez les logs: docker-compose logs flask_app"
fi

# Afficher les informations de connexion
info "Déploiement terminé!"
echo ""
echo "Services disponibles:"
echo "  - Application Flask: http://localhost:${APP_PORT:-5000}"
if [ "$ENV" = "production" ]; then
    echo "  - Nginx HTTP: http://localhost:${NGINX_HTTP_PORT:-80}"
    echo "  - Nginx HTTPS: https://localhost:${NGINX_HTTPS_PORT:-443}"
fi
echo "  - PostgreSQL: localhost:${POSTGRES_PORT:-5432}"
echo "  - Redis: localhost:${REDIS_PORT:-6379}"
echo ""
echo "Commandes utiles:"
echo "  - Voir les logs: docker-compose logs -f"
echo "  - Arrêter: docker-compose down"
echo "  - Redémarrer: docker-compose restart"
echo "  - Statut: docker-compose ps"
