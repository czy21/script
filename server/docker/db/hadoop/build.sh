#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
dir_name="$(basename ${dir})"

source ${dir}/../../.env.global



docker build --tag ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/${dir_name} --file ${dir}/Dockerfile ${dir}/
docker push ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/${dir_name}


