#!/bin/bash

cd $(cd "$(dirname "$0")"; pwd)
source ./openwrt-build-config.sh
container_name=openwrt-target-${branch}
status=$(docker inspect --format='{{.State.Running}}' ${container_name} 2>/dev/null)

if [ -z "$status" ];then
  docker run --detach -it --user buildbot --workdir /builder --name ${container_name} --entrypoint "" \
    -v ${container_name}:/builder \
    -v openwrt-share:/data \
    -v $source:/ci openwrt/tools$([ "$branch" = 'main' ] || echo ":$branch") /bin/bash
fi

if [ "$status" = "false" ];then
  docker start ${container_name}
fi

docker exec -e mirror=$mirror -e origin=$origin -e branch=$branch -i ${container_name} bash -s -- "$@" < ./$(basename $0 | sed 's|-exec||')