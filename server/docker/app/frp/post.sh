#!/bin/bash

set -e




sudo docker network connect nginx_default frp

sudo cp -r $dir/nginx/frp.conf ${param_config_dir}/nginx/conf.d/

sudo docker restart nginx