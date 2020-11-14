#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)

sudo docker network connect nginx_default frp

sudo cp -r $dir/nginx/frp.conf /data/config/nginx/conf.d/

sudo docker restart nginx