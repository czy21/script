#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

docker build --tag ${GLOBAL_REGISTRY_URL}/confluence:1.0 --file ${dir}/image/confluence-dockerfile ${dir}/image/ --no-cache --force-rm
docker build --tag ${GLOBAL_REGISTRY_URL}/jira:1.0 --file ${dir}/image/jira-dockerfile ${dir}/image/ --no-cache --force-rm

#docker login ${GLOBAL_REGISTRY_URL} --username admin --password Czy20210314.
docker push ${GLOBAL_REGISTRY_URL}/confluence:1.0
docker push ${GLOBAL_REGISTRY_URL}/jira:1.0
#docker logout