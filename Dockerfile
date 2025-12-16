# Dockerfile pour l'application Flask BoursA
# Image de base Python 3.11 (LTS)
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="BoursA Team"
LABEL description="Application Flask d'analyse de données et Machine Learning"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Créer un utilisateur non-root pour la sécurité
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copier le code de l'application
COPY . .

# Copier et rendre exécutable le script d'entrypoint
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Créer les répertoires nécessaires avec les bonnes permissions
RUN mkdir -p uploads logs app/models && \
    chown -R appuser:appuser /app

# Passer à l'utilisateur non-root
USER appuser

# Exposer le port 5000
EXPOSE 5000

# Health check (utilise curl qui est disponible dans l'image alpine ou wget)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health', timeout=5)" || exit 1

# Entrypoint pour initialiser la base avant de démarrer
ENTRYPOINT ["/entrypoint.sh"]

# Commande par défaut (peut être surchargée dans docker-compose)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]

