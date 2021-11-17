#!/bin/bash

set -e

docker build --tag ${param_registry_url}/${param_registry_dir}/${param_role_name} --file ${param_role_path}/Dockerfile ${param_role_path}/
docker push ${param_registry_url}/${param_registry_dir}/${param_role_name}

docker build --tag ${param_registry_url}/${param_registry_dir}/${dir_name}-web --file ${dir}/web/Dockerfile ${dir}/web/
docker push ${param_registry_url}/${param_registry_dir}/${param_role_name}-web



