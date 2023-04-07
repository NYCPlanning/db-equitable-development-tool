#!/bin/bash
#
# Sets up enviroment for running build scripts in either local devcontainer or github action.
set -e

apt-get update

# Install R
apt-get -y install r-base

# Install python packages
python3 -m pip install --upgrade pip
python3 -m pip install --requirement requirements.txt

# Install required R package
Rscript -e "install.packages('survey')"
