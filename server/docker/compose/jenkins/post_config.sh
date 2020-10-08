#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
container_name="jenkins"
sudo docker exec -i ${container_name} bash -c "sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
                                            && apk update"

sudo docker exec -i ${container_name} bash -c "apk add python3"