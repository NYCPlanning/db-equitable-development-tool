# See here for base image contents: https://github.com/devcontainers/images/tree/main/src/python
ARG VARIANT="3.9"
FROM mcr.microsoft.com/devcontainers/python:0-${VARIANT}

RUN export DEBIAN_FRONTEND=noninteractive

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# Run environment setup script
COPY utils/ utils/
COPY requirements.txt .
COPY .env .
RUN utils/setup_build_env.sh