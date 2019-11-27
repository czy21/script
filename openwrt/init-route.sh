#!/bin/bash

ash -c "set -e;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com > /etc/dropbear/authorized_keys"

wget http://openwrt-dist.sourceforge.net/packages/openwrt-dist.pub -P /root/
opkg-key add /root/openwrt-dist.pub
rm /root/openwrt-dist.pub

sed -i 's/openwrt.proxy.ustclug.org/downloads.openwrt.org/g' /etc/opkg/distfeeds.conf;

tee /etc/opkg/customfeeds.conf <<-'EOF'
src/gz openwrt_dist http://openwrt-dist.sourceforge.net/packages/base/mipsel_24kc
src/gz openwrt_dist_luci http://openwrt-dist.sourceforge.net/packages/luci
EOF
opkg update
#opkg install openssh-client
#luci-i18n-base-zh-cn coreutils-nohup openssh-client ChinaDNS luci-app-chinadns redsocks