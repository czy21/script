#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

docker build --tag ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/confluence --file ${dir}/Dockerfile-Confluence ${dir}/ --no-cache --force-rm
docker build --tag ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/jira --file ${dir}/Dockerfile-Jira ${dir}/ --no-cache --force-rm

docker login ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR} --username admin --password Czy20210314.
docker push ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/confluence
docker push ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/jira