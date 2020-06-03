#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
sudo rm -rf /data/config/nginx/conf.d/
sudo cp -r $dir/cert/ /data/config/nginx/
sudo cp -r $dir/conf.d/ /data/config/nginx/
sudo docker restart nginx