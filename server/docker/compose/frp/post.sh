#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

sudo docker network connect nginx_default frp

sudo cp -r $dir/nginx/frp.conf ${GLOBAL_CONFIG_DIR}/nginx/conf.d/

sudo docker restart nginx