#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
dir_name="$(basename ${dir})"

source ${dir}/../../.env.global



docker build --tag ${param_registry_url}/${param_registry_dir}/${dir_name} --file ${dir}/Dockerfile ${dir}/
docker push ${param_registry_url}/${param_registry_dir}/${dir_name}

docker build --tag ${param_registry_url}/${param_registry_dir}/${dir_name}-web --file ${dir}/web/Dockerfile ${dir}/web/
docker push ${param_registry_url}/${param_registry_dir}/${dir_name}-web



