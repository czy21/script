#!/bin/bash

set -x
mirror=${mirror:-'https://openwrt-dlc.czy21.com/openwrt'}
origin=${origin:-'https://gitea.czy21.com:8443'}
branch=${branch:-'main'}
target=${1:-'x86/64'}
source=/mnt/c/Users/bruce/Desktop/dev/gitea-project/czy21/openwrt-plugin
set +x