#!/bin/bash

ash -c "set -e;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com > /etc/dropbear/authorized_keys"

# network start

uci set network.lan.ipaddr='192.168.2.2'
uci set network.lan.gateway='192.168.2.1'
uci set network.lan.dns='114.114.114.114 223.5.5.5 192.168.2.2'
uci commit network

# network end

# dnsmasq start

uci add_list dhcp.@dnsmasq[0].address="/internal-home.com/192.168.2.21"
uci commit dhcp

# dnsmasq end

reboot