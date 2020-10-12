#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
container_name="jenkins"
sudo docker exec -i ${container_name} bash < $dir/install_tool.sh

# /server/install_tool.sh
#sudo docker exec -i ${container_name} bash < ../../../install_tool.sh