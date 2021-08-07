#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

docker build --tag registry:5000/hbase --file ${dir}/Dockerfile ${dir}/

docker push registry:5000/hbase

docker image prune -f