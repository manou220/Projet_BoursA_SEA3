#!/bin/bash
# Script pour générer des certificats SSL auto-signés pour le développement
# Usage: ./scripts/generate_ssl_certs.sh [domain]

set -e

DOMAIN=${1:-localhost}
SSL_DIR="nginx/ssl"

info() {
    echo "[INFO] $1"
}

# Créer le répertoire SSL
mkdir -p "$SSL_DIR"

info "Génération de certificats SSL auto-signés pour $DOMAIN..."

# Générer la clé privée
openssl genrsa -out "$SSL_DIR/key.pem" 2048

# Générer le certificat
openssl req -new -x509 -key "$SSL_DIR/key.pem" -out "$SSL_DIR/cert.pem" -days 365 \
    -subj "/C=FR/ST=State/L=City/O=BoursA/CN=$DOMAIN"

# Définir les permissions appropriées
chmod 600 "$SSL_DIR/key.pem"
chmod 644 "$SSL_DIR/cert.pem"

info "✅ Certificats générés avec succès dans $SSL_DIR/"
info "⚠️  Ces certificats sont auto-signés et ne doivent être utilisés qu'en développement"
info "   Pour la production, utilisez Let's Encrypt ou des certificats signés par une autorité de certification"

