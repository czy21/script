#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../.env.global

sudo rm -rf ${GLOBAL_CONFIG_DIR}/zookeeper/
sudo mkdir -p ${GLOBAL_CONFIG_DIR}/zookeeper/

sudo cp -r $dir/zookeeper_conf/* ${GLOBAL_CONFIG_DIR}/zookeeper/

sudo rm -rf ${GLOBAL_CONFIG_DIR}/kafka_eagle/
sudo mkdir -p ${GLOBAL_CONFIG_DIR}/kafka_eagle/

sudo cp -r $dir/kafka_eagle/conf/* ${GLOBAL_CONFIG_DIR}/kafka_eagle/