#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
dir_name="$(basename ${dir})"

source ${dir}/../../.env.global

docker build --tag registry:5000/${dir_name} --file ${dir}/Dockerfile ${dir}/

docker push registry:5000/${dir_name}

#docker image prune --force --all