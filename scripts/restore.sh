#!/bin/bash
# Script de restauration pour BoursA
# Usage: ./scripts/restore.sh <backup_directory>

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <backup_directory>"
    echo "Exemple: $0 ./backups/backup_20250101_120000"
    exit 1
fi

BACKUP_PATH="$1"

if [ ! -d "$BACKUP_PATH" ]; then
    echo "[ERROR] Le répertoire de backup n'existe pas: $BACKUP_PATH"
    exit 1
fi

info() {
    echo "[INFO] $1"
}

warn() {
    echo "[WARN] $1"
}

# Confirmation
read -p "Êtes-vous sûr de vouloir restaurer depuis $BACKUP_PATH? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Restauration annulée"
    exit 0
fi

info "Démarrage de la restauration..."

# Restaurer la base de données
if [ -f "$BACKUP_PATH/database.sql" ]; then
    info "Restauration de la base de données PostgreSQL..."
    if docker ps | grep -q boursa_postgres; then
        docker exec -i boursa_postgres psql -U ${POSTGRES_USER:-boursa_user} ${POSTGRES_DB:-boursa} < "$BACKUP_PATH/database.sql" || {
            error "Échec de la restauration de la base de données"
            exit 1
        }
        info "✅ Base de données restaurée"
    else
        error "PostgreSQL n'est pas en cours d'exécution"
        exit 1
    fi
else
    warn "⚠️  Fichier de sauvegarde de la base de données non trouvé"
fi

# Restaurer les uploads
if [ -f "$BACKUP_PATH/uploads.tar.gz" ]; then
    info "Restauration des fichiers uploadés..."
    tar -xzf "$BACKUP_PATH/uploads.tar.gz" || {
        error "Échec de la restauration des uploads"
        exit 1
    }
    info "✅ Uploads restaurés"
fi

# Restaurer les modèles ML
if [ -f "$BACKUP_PATH/models.tar.gz" ]; then
    info "Restauration des modèles ML..."
    tar -xzf "$BACKUP_PATH/models.tar.gz" || {
        error "Échec de la restauration des modèles"
        exit 1
    }
    info "✅ Modèles restaurés"
fi

# Restaurer les logs (optionnel)
if [ -f "$BACKUP_PATH/logs.tar.gz" ]; then
    info "Restauration des logs..."
    tar -xzf "$BACKUP_PATH/logs.tar.gz" || {
        warn "⚠️  Échec de la restauration des logs (non critique)"
    }
fi

info "✅ Restauration terminée"
warn "⚠️  N'oubliez pas de vérifier la configuration (.env) si nécessaire"

