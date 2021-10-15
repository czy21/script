#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
dir_name="$(basename ${dir})"

source ${dir}/../../.env.global

docker login ${GLOBAL_REGISTRY_URL} --username ${GLOBAL_REGISTRY_USERNAME} --password ${GLOBAL_REGISTRY_PASSWORD}

docker build --tag ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/${dir_name} --file ${dir}/Dockerfile ${dir}/
docker push ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/${dir_name}

docker build --tag ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/${dir_name}-web --file ${dir}/web/Dockerfile ${dir}/web/
docker push ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/${dir_name}-web



