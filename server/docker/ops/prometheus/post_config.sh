#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global
container_name="prometheus"

sudo cat $dir/nginx/nginx.conf > ${GLOBAL_CONFIG_DIR}/nginx/conf.d/${container_name}.conf

sudo docker exec -i nginx nginx -s reload