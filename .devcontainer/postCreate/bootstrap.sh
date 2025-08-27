#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="/workspaces/${LOCAL_NAME:-${PWD##*/}}"
cd "$PROJECT_ROOT"

log() { echo -e "[bootstrap] $1"; }
has() { command -v "$1" >/dev/null 2>&1; }

log "Detecting project layout..."

if [ -f "pyproject.toml" ]; then
  log "Python project detected (pyproject.toml)."
  if ! has uv; then
    log "Installing uv (fast Python package manager)..."
    curl -fsSL https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
  fi
  if [ -f "requirements.txt" ]; then
    log "Creating venv and installing requirements.txt with uv..."
    uv venv .venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
  else
    log "Creating venv and syncing from pyproject with uv..."
    uv venv .venv
    source .venv/bin/activate
    uv pip install -e . || true
    uv pip install -r requirements-dev.txt || true
  fi
fi

if [ -f "package.json" ]; then
  log "Node project detected (package.json)."
  if ! has pnpm; then
    corepack enable || true
    corepack prepare pnpm@latest --activate || true
  fi
  if has pnpm; then
    pnpm install --frozen-lockfile || pnpm install
  else
    npm ci || npm install
  fi
fi

if [ -f ".pre-commit-config.yaml" ]; then
  log "Installing pre-commit hooks..."
  if ! has pre-commit; then
    pip install --user pre-commit
  fi
  pre-commit install
fi

log "Bootstrap complete."
