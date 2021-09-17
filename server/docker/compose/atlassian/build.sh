#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

docker build --tag ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/confluence --file ${dir}/image/confluence-dockerfile ${dir}/image/ --no-cache --force-rm
docker build --tag ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/jira --file ${dir}/image/jira-dockerfile ${dir}/image/ --no-cache --force-rm

docker login ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR} --username admin --password ***REMOVED***
docker push ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/confluence
docker push ${GLOBAL_REGISTRY_URL}/${GLOBAL_REGISTRY_DIR}/jira