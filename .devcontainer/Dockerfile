# syntax=docker/dockerfile:1.6
FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# System deps you had
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
        ca-certificates \
        pkg-config \
        libssl-dev \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
        libatlas-base-dev \
        gfortran \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Your helper scripts (keep as-is)
COPY .devcontainer/library-scripts/ /usr/local/share/devcontainer/library-scripts/
RUN chmod -R 755 /usr/local/share/devcontainer/library-scripts

# Install Python deps (no venv, global inside image)
COPY requirements.txt /tmp/pip-tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

# Workspace setup (same as before)
RUN mkdir -p /workspaces && chown -R vscode:vscode /workspaces

USER vscode
WORKDIR /workspaces
SHELL ["/bin/bash", "-lc"]
