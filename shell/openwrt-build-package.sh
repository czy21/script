#!/bin/bash
pkg=$2
[ -f "feeds.conf.default.bak" ] || cp -rv feeds.conf.default feeds.conf.default.bak
sed -e "s|https://git.openwrt.org/\(.*\)/|$origin/openwrt/|g" \
    -e "s|https://github.com/openwrt/|$origin/openwrt/|g" \
    -e "s|\^.*|;$branch|" feeds.conf.default.bak > feeds.conf.default

echo 'src-link ci /ci/' >> feeds.conf.default
./scripts/feeds update -a
make defconfig
./scripts/feeds install -p ci -f -a

make -j1 package/$pkg/${2:-compile}
ls -al bin/packages/x86_64/ci/ 2>/dev/null || true