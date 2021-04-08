#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

sudo docker network connect nginx_default v2ray

sudo cp -r $dir/nginx/v2ray.conf ${GLOBAL_CONFIG_DIR}/nginx/conf.d/

sudo docker restart nginx