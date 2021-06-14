#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global
container_name="nginx"

sudo cp -r $dir/post/conf.d/* ${GLOBAL_CONFIG_DIR}/nginx/conf.d/

sudo docker exec -i ${container_name} nginx -s reload