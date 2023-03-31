#!/bin/bash
#
# Sets up enviroment for dev in local devcontainer.
set -e

# Skip when called in a github action workflow
if [[ !$CI == "true" ]]; then
    # Add id_rsa so that we can push to github from the dev container
    # ssh-add $HOME/.ssh/id_rsa
    ssh-add
fi
