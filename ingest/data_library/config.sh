#!/bin/bash

function set_env {
  envfile=$1
    if [ -f $envfile ];
    then
        export $(cat $envfile | xargs)
    fi
}
# Set Environmental variables
set_env .env 
