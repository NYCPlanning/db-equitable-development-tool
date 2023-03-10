# See here for image contents: https://github.com/NYCPlanning/docker-geosupport

# [Choice] Geosupport version
# ARG VARIANT="latest"
FROM nycplanning/docker-geosupport:latest

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# Run environment setup script
COPY utils/ utils/
COPY requirements.txt .
RUN utils/setup_build_env.sh