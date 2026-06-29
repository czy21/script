#!/bin/bash

cd $(cd "$(dirname "$0")"; pwd)

pkg=$1
branch="openwrt-25.12"
target="x86-64"
volume=/mnt/c/Users/bruce/Desktop/dev/gitea-project/czy21/openwrt-plugin
status=$(docker inspect --format='{{.State.Running}}' openwrt-sdk-${target}-${branch}-dev 2>/dev/null)

if [ -z "$status" ];then
  docker run --detach -it --name openwrt-sdk-${target}-${branch}-dev -v openwrt-sdk-${target}-${branch}-dev:/builder -v openwrt-share:/data -v $volume:/builder/ci openwrt/sdk:${target}-$(echo $branch | sed 's|openwrt-||').0
fi

if [ "$status" = "false" ];then
  docker start openwrt-sdk-${target}-${branch}-dev
fi

docker exec -i openwrt-sdk-${target}-${branch}-dev bash <<EOF
  [ ! -f "feeds.conf.default.bak" ] && cp -rv feeds.conf.default feeds.conf.default.bak
  sed -e 's|https://git.openwrt.org/\(.*\)/|https://gitea.czy21.com:8443/openwrt/|g' \
      -e 's|https://github.com/openwrt/|https://gitea.czy21.com:8443/openwrt/|g' \
      -e "s|\^.*|;$branch|" feeds.conf.default.bak > feeds.conf.default
  
  echo 'src-link ci /builder/ci/' >> feeds.conf.default
  ./scripts/feeds update -a
  make defconfig
  ./scripts/feeds install -p ci -f -a

  make -j1 package/$pkg/${2:-compile}
  ls -al bin/packages/x86_64/ci/ 2>/dev/null || true
EOF