SHELL := /bin/bash

.PHONY: dev rebuild stop bash logs

dev:
	@echo "Opening in Dev Container..."
	@code -n . || true

rebuild:
	docker compose -f .devcontainer/docker-compose.yml build --no-cache

stop:
	docker compose -f .devcontainer/docker-compose.yml down

bash:
	docker compose -f .devcontainer/docker-compose.yml exec dev bash || true

logs:
	docker compose -f .devcontainer/docker-compose.yml logs -f dev
