#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

docker build --tag registry:5000/ubuntu:18.04 --file ${dir}/Dockerfile ${dir}/ --no-cache --force-rm

#docker login registry:5000 --username admin --password ***REMOVED***
docker push registry:5000/ubuntu:18.04
#docker logout