#!/bin/bash
# Script de maintenance pour BoursA
# Usage: ./scripts/maintenance.sh [clean|logs|stats|update]

set -e

ACTION=${1:-help}

info() {
    echo "[INFO] $1"
}

warn() {
    echo "[WARN] $1"
}

error() {
    echo "[ERROR] $1" >&2
}

case "$ACTION" in
    clean)
        info "Nettoyage des ressources Docker..."
        docker-compose down -v 2>/dev/null || docker compose down -v 2>/dev/null || true
        docker system prune -f
        info "✅ Nettoyage terminé"
        ;;
    
    logs)
        info "Affichage des logs (Ctrl+C pour quitter)..."
        docker-compose logs -f || docker compose logs -f
        ;;
    
    stats)
        info "Statistiques des conteneurs:"
        docker stats --no-stream
        echo ""
        info "Utilisation des volumes:"
        docker volume ls | grep boursa || true
        ;;
    
    update)
        info "Mise à jour de l'application..."
        docker-compose pull || docker compose pull
        docker-compose build || docker compose build
        docker-compose up -d || docker compose up -d
        info "✅ Mise à jour terminée"
        ;;
    
    restart)
        info "Redémarrage des services..."
        docker-compose restart || docker compose restart
        info "✅ Services redémarrés"
        ;;
    
    health)
        info "Vérification de la santé des services..."
        echo ""
        
        # PostgreSQL
        if docker exec boursa_postgres pg_isready -U ${POSTGRES_USER:-boursa_user} &> /dev/null; then
            echo "✅ PostgreSQL: OK"
        else
            echo "❌ PostgreSQL: ERREUR"
        fi
        
        # Redis
        if docker exec boursa_redis redis-cli ping &> /dev/null; then
            echo "✅ Redis: OK"
        else
            echo "⚠️  Redis: Vérification échouée (peut être normal si mot de passe requis)"
        fi
        
        # Flask App
        if curl -f http://localhost:${APP_PORT:-5000}/health &> /dev/null; then
            echo "✅ Flask App: OK"
        else
            echo "❌ Flask App: ERREUR"
        fi
        ;;
    
    help|*)
        echo "Usage: $0 [action]"
        echo ""
        echo "Actions disponibles:"
        echo "  clean    - Nettoyer les ressources Docker"
        echo "  logs     - Afficher les logs en temps réel"
        echo "  stats    - Afficher les statistiques"
        echo "  update   - Mettre à jour l'application"
        echo "  restart  - Redémarrer les services"
        echo "  health   - Vérifier la santé des services"
        echo "  help     - Afficher cette aide"
        ;;
esac

