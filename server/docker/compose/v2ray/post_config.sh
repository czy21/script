#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)

sudo docker network connect nginx_default v2ray

sudo cp -r $dir/nginx/v2ray.conf /data/config/nginx/conf.d/

sudo docker restart nginx