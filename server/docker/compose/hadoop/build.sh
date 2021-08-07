#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

docker build --tag registry:5000/hadoop --file ${dir}/Dockerfile ${dir}/

docker push registry:5000/hadoop

docker image prune -f