#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)

sudo rm -rf /data/config/zookeeper/
sudo mkdir -p /data/config/zookeeper/

sudo cp -r $dir/zookeeper_conf/* /data/config/zookeeper/

sudo rm -rf /data/config/kafka_eagle/
sudo mkdir -p /data/config/kafka_eagle/

sudo cp -r $dir/kafka_eagle/conf/* /data/config/kafka_eagle/