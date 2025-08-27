# syntax=docker/dockerfile:1.6
ARG VARIANT=bookworm
FROM mcr.microsoft.com/devcontainers/base:${VARIANT}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update         && apt-get install -y --no-install-recommends            build-essential            git            curl            ca-certificates            pkg-config            libssl-dev            libffi-dev            libxml2-dev libxslt1-dev            libatlas-base-dev gfortran            wget         && rm -rf /var/lib/apt/lists/*

COPY .devcontainer/library-scripts/ /usr/local/share/devcontainer/library-scripts/
RUN chmod -R 755 /usr/local/share/devcontainer/library-scripts

RUN mkdir -p /workspaces && chown -R vscode:vscode /workspaces

USER vscode
WORKDIR /workspaces

SHELL ["/bin/bash", "-lc"]
