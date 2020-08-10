#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
config_path=/data/config/portainer/

sudo mkdir -p ${config_path}

sudo cp -r $dir/conf/* ${config_path}