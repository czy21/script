#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global
container_name="nginx"

#sudo cat $dir/nginx/ops.conf > ${GLOBAL_CONFIG_DIR}/nginx/conf.d/${container_name}.conf

for f in $(ls ${dir}/post/*.conf); do
  cat $f > ${GLOBAL_CONFIG_DIR}/nginx/conf.d/${container_name}.conf
done

#sudo docker exec -i nginx nginx -s reload