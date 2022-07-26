# See here for image contents: https://github.com/NYCPlanning/docker-geosupport

# [Choice] Geosupport version
# ARG VARIANT="latest"
FROM nycplanning/docker-geosupport:latest

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
RUN apt-get update
#Install R
RUN apt-get -y install r-base
# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
ENV PATH="~/.poetry/bin:$PATH"
ENV PATH="~/.local/bin:$PATH"

RUN /usr/local/bin/python3 -m pip install -U flake8
RUN /usr/local/bin/python3 -m pip install -U black
