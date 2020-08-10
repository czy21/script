#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)

volume_path=/data/volumes/neo4j/
config_path=/data/config/neo4j/

sudo mkdir -p ${config_path}
sudo mkdir -p ${volume_path}

sudo cp -r $dir/conf/ ${config_path}