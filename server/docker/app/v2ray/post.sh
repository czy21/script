#!/bin/bash

set -e




sudo docker network connect nginx_default v2ray

sudo cp -r $dir/nginx/v2ray.conf ${param_config_dir}/nginx/conf.d/

sudo docker restart nginx