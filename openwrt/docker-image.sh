#!/bin/bash

docker run -d -it -p 8080:80 --name openwrt openwrt-x86-generic-rootfs /bin/ash