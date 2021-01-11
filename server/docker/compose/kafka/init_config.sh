#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)

sudo rm -rf /data/config/zookeeper/
sudo mkdir -p /data/config/zookeeper/conf/

sudo cp -r $dir/zookeeper_conf/* /data/config/zookeeper/