FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p uploads app/models

# Exposer le port
EXPOSE 5000

# Variable d'environnement
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production

# Créer le dossier pour la base de données
RUN mkdir -p /app/data

# Commande de démarrage
CMD ["python", "wsgi.py"]
