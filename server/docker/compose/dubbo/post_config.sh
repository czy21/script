#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../.env.global

sudo docker network connect dubbo_default zookeeper1
sudo docker network connect dubbo_default zookeeper2
sudo docker network connect dubbo_default zookeeper3