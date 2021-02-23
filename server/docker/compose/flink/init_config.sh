#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../.env.global

sudo rm -rf ${GLOBAL_VOLUMES_DIR}/jobmanager/
sudo mkdir -p ${GLOBAL_VOLUMES_DIR}/jobmanager/

sudo cp -r $dir/___temp/jar/* ${GLOBAL_VOLUMES_DIR}/jobmanager/