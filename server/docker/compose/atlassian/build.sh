#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

docker build --tag ${GLOBAL_REGISTRY_URL}/confluence --file ${dir}/image/confluence-dockerfile ${dir}/image/ --no-cache --force-rm
docker build --tag ${GLOBAL_REGISTRY_URL}/jira --file ${dir}/image/jira-dockerfile ${dir}/image/ --no-cache --force-rm

#docker login ${GLOBAL_REGISTRY_URL} --username admin --password ***REMOVED***
docker push ${GLOBAL_REGISTRY_URL}/confluence
docker push ${GLOBAL_REGISTRY_URL}/jira
#docker logout