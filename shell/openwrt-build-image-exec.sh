#!/bin/bash

cd $(cd "$(dirname "$0")"; pwd)
source ./openwrt-build-config.sh
container_name=openwrt-ib-$(echo $target | sed 's|/|-|')-${branch}-dev
status=$(docker inspect --format='{{.State.Running}}' ${container_name} 2>/dev/null)

if [ -z "$status" ];then
  set -x
  docker run --detach -it --name ${container_name} \
    -v ${container_name}:/builder \
    -v openwrt-share:/data \
    -v $source:/ci openwrt/imagebuilder:x86-64-$branch
fi

if [ "$status" = "false" ];then
  docker start ${container_name}
fi

docker exec \
  -e mirror=$mirror -e origin=$origin -e branch=$branch -e TARGET=$target \
  -e UPSTREAM_URL=$UPSTREAM_URL -e VERSION_PATH=$VERSION_PATH \
  -i ${container_name} bash -s -- "$@" < ./$(basename $0 | sed 's|-exec||')