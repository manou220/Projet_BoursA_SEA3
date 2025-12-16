#!/bin/bash
# Script de sauvegarde pour BoursA
# Usage: ./scripts/backup.sh [backup_directory]

set -e

BACKUP_DIR=${1:-./backups}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="$BACKUP_DIR/backup_$TIMESTAMP"

info() {
    echo "[INFO] $1"
}

error() {
    echo "[ERROR] $1" >&2
}

# Créer le répertoire de backup
mkdir -p "$BACKUP_PATH"

info "Démarrage de la sauvegarde..."

# Sauvegarder la base de données PostgreSQL
if docker ps | grep -q boursa_postgres; then
    info "Sauvegarde de la base de données PostgreSQL..."
    docker exec boursa_postgres pg_dump -U ${POSTGRES_USER:-boursa_user} ${POSTGRES_DB:-boursa} > "$BACKUP_PATH/database.sql" || {
        error "Échec de la sauvegarde de la base de données"
        exit 1
    }
    info "✅ Base de données sauvegardée"
else
    warn "⚠️  PostgreSQL n'est pas en cours d'exécution. Sauvegarde de la base de données ignorée."
fi

# Sauvegarder les uploads
if [ -d "uploads" ] && [ "$(ls -A uploads 2>/dev/null)" ]; then
    info "Sauvegarde des fichiers uploadés..."
    tar -czf "$BACKUP_PATH/uploads.tar.gz" uploads/ || {
        error "Échec de la sauvegarde des uploads"
        exit 1
    }
    info "✅ Uploads sauvegardés"
fi

# Sauvegarder les modèles ML
if [ -d "app/models" ] && [ "$(ls -A app/models 2>/dev/null)" ]; then
    info "Sauvegarde des modèles ML..."
    tar -czf "$BACKUP_PATH/models.tar.gz" app/models/ || {
        error "Échec de la sauvegarde des modèles"
        exit 1
    }
    info "✅ Modèles sauvegardés"
fi

# Sauvegarder les logs (optionnel)
if [ -d "logs" ] && [ "$(ls -A logs 2>/dev/null)" ]; then
    info "Sauvegarde des logs..."
    tar -czf "$BACKUP_PATH/logs.tar.gz" logs/ || {
        warn "⚠️  Échec de la sauvegarde des logs (non critique)"
    }
fi

# Sauvegarder la configuration
info "Sauvegarde de la configuration..."
cp .env "$BACKUP_PATH/.env" 2>/dev/null || warn "⚠️  Fichier .env non trouvé"
cp docker-compose.yml "$BACKUP_PATH/" 2>/dev/null || true
cp Dockerfile "$BACKUP_PATH/" 2>/dev/null || true

# Créer un fichier d'information
cat > "$BACKUP_PATH/backup_info.txt" << EOF
Sauvegarde BoursA
Date: $(date)
Version: 1.0.0
Contenu:
- Base de données PostgreSQL
- Fichiers uploadés
- Modèles ML
- Logs
- Configuration
EOF

info "✅ Sauvegarde terminée: $BACKUP_PATH"
info "Taille totale: $(du -sh "$BACKUP_PATH" | cut -f1)"
