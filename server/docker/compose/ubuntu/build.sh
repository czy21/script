#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

docker build --tag ${GLOBAL_REGISTRY_URL}/ubuntu:18.04 --file ${dir}/Dockerfile ${dir}/ --no-cache --force-rm
docker push ${GLOBAL_REGISTRY_URL}/ubuntu:18.04