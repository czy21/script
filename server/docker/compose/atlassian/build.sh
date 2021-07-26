#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

docker build --tag registry:5000/confluence:1.0 --file ${dir}/image/confluence-dockerfile ${dir}/image/ --no-cache --force-rm
docker build --tag registry:5000/jira:1.0 --file ${dir}/image/jira-dockerfile ${dir}/image/ --no-cache --force-rm

#docker login registry:5000 --username admin --password Czy20210314.
docker push registry:5000/confluence:1.0
docker push registry:5000/jira:1.0
#docker logout