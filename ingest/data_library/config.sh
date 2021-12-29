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

function get_version {
  local name=$1
  local config_path=spaces/edm-recipes/datasets/$name/latest/config.json
  local version=$(mc cat $config_path | jq -r '.dataset.version')
  echo "$version"
}

function import_csv {
  local name=$1
  local version=$(get_version $name)
  local target_dir=.library/$name/$version
  echo $target_dir
  if [ -f $target_dir/$name.csv ]; then
    echo "✅ $name.csv exists in cache"
  else
    echo "🛠 $name.csv doesn't exists in cache, downloading ..."
    mkdir -p $target_dir 
    mc cp spaces/edm-recipes/datasets/$name/latest/$name.csv $target_dir/$name.csv
  fi
}