# Makefile pour BoursA
# Simplifie les commandes de déploiement et maintenance

.PHONY: help build up down restart logs clean backup deploy test

# Variables
COMPOSE_FILE = docker-compose.yml
ENV_FILE = .env

help: ## Affiche cette aide
	@echo "Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Construire les images Docker
	docker-compose -f $(COMPOSE_FILE) build || docker compose -f $(COMPOSE_FILE) build

up: ## Démarrer les services
	docker-compose -f $(COMPOSE_FILE) up -d || docker compose -f $(COMPOSE_FILE) up -d

up-nginx: ## Démarrer les services avec Nginx
	docker-compose -f $(COMPOSE_FILE) --profile nginx up -d || docker compose -f $(COMPOSE_FILE) --profile nginx up -d

down: ## Arrêter les services
	docker-compose -f $(COMPOSE_FILE) down || docker compose -f $(COMPOSE_FILE) down

restart: ## Redémarrer les services
	docker-compose -f $(COMPOSE_FILE) restart || docker compose -f $(COMPOSE_FILE) restart

logs: ## Afficher les logs
	docker-compose -f $(COMPOSE_FILE) logs -f || docker compose -f $(COMPOSE_FILE) logs -f

status: ## Afficher le statut des services
	docker-compose -f $(COMPOSE_FILE) ps || docker compose -f $(COMPOSE_FILE) ps

health: ## Vérifier l'état de santé
	curl -f http://localhost:5000/health || echo "Service non disponible"

backup: ## Créer une sauvegarde
	bash scripts/backup.sh

deploy: ## Déployer l'application
	bash scripts/deploy.sh

clean: ## Nettoyer les images et volumes Docker inutilisés
	docker system prune -f
	docker volume prune -f

test: ## Exécuter les tests
	pytest tests/ -v

install-dev: ## Installer les dépendances de développement
	pip install -r requirements.txt
	@if [ "$$(uname -s)" = "MINGW"* ] || [ "$$(uname -s)" = "MSYS"* ] || [ "$$(uname -s)" = "CYGWIN"* ]; then \
		pip install -r requirements-windows.txt; \
	fi

setup-env: ## Créer le fichier .env à partir du template
	@if [ ! -f $(ENV_FILE) ]; then \
		cp ENV_EXAMPLE.txt $(ENV_FILE); \
		echo "✅ Fichier .env créé. Veuillez le configurer avant de déployer."; \
	else \
		echo "⚠️  Le fichier .env existe déjà."; \
	fi

