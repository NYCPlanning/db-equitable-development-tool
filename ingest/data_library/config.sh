#!/bin/bash

function set_env {
  envfile=$1
    if [ -f $envfile ];
    then
        export $(cat $envfile | xargs)
        mc config host add spaces $AWS_S3_ENDPOINT $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY --api S3v4
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
  local version=${2:-latest}
  local dataset=$1
  if [ $version == "latest" ]; then
    local filename=$dataset
  else
    local filename="${dataset}_${version}"
  fi
  local target_dir=.library
  echo $target_dir
  if [ -f $target_dir/$filename.csv ]; then
    echo "✅ $filename.csv exists in cache"
  else
    echo "🛠 $filename.csv doesn't exist in cache, downloading ..."
    mkdir -p $target_dir 
    mc cp spaces/edm-recipes/datasets/$dataset/$version/$dataset.csv $target_dir/$filename.csv
  fi
}