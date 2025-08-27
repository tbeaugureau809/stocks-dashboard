# Dev Container

This container is designed to be reused across projects. It auto-detects Python (yfinance, Dash/Streamlit) and/or Node (Next/Vite) workflows and bootstraps them.

## Use
1. Copy `.devcontainer/`, `.vscode/`, `Makefile`, and `.env.example` into your repo root.
2. In VS Code, run **Dev Containers: Reopen in Container**.
3. The `postCreate` script sets up Python/Node deps if it finds `pyproject.toml` or `package.json`.

## Ports
- 8050 (Dash), 8501 (Streamlit), 8888 (Jupyter), 3000 (web), 5000/8000 (APIs)

## Services
Optional Postgres/Redis services are defined in `docker-compose.yml`. Uncomment if needed.
