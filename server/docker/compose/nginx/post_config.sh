#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
sudo rm -rf /data/config/nginx/conf.d/
sudo cp -r $dir/override/cert/ /data/config/nginx/
sudo cp -r $dir/override/conf.d/ /data/config/nginx/
sudo docker restart nginx