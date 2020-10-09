#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
container_name="jenkins"
sudo docker exec -i ${container_name} bash -c "sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
                                            && apk update"

sudo docker exec -i ${container_name} bash -c "apk add python3 py3-pip"

sudo docker exec -i ${container_name} bash -c "mkdir ~/.pip/ && tee ~/.pip/pip.conf <<-'EOF'
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
EOF"