#!/bin/bash

ash -c "set -e;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com > /etc/dropbear/authorized_keys"

# network
uci set network.lan.ipaddr=192.168.2.2
uci set network.lan.gateway=192.168.2.1
uci set network.lan.dns=114.114.114.114
uci commit network

# google clound
uci add shadowsocksr servers
uci set shadowsocksr.@servers[0].alias='gg_hk'
uci set shadowsocksr.@servers[0].type='v2ray'
uci set shadowsocksr.@servers[0].server='34.96.138.30'
uci set shadowsocksr.@servers[0].server_port='40879'
uci set shadowsocksr.@servers[0].alter_id='4'
uci set shadowsocksr.@servers[0].vmess_id='e85f98fb-83b4-4234-a51f-85df46403a8e'
uci set shadowsocksr.@servers[0].local_port='1234'
uci set shadowsocksr.@servers[0].security='auto'
uci set shadowsocksr.@servers[0].transport='tcp'
uci set shadowsocksr.@servers[0].tcp_guise='http'
uci set shadowsocksr.@servers[0].switch_enable='0'

# ali clound
uci add shadowsocksr servers
uci set shadowsocksr.@servers[1].alias='ali_hk'
uci set shadowsocksr.@servers[1].type='v2ray'
uci set shadowsocksr.@servers[1].server='149.129.125.40'
uci set shadowsocksr.@servers[1].server_port='40879'
uci set shadowsocksr.@servers[1].alter_id='64'
uci set shadowsocksr.@servers[1].vmess_id='e85f98fb-83b4-4234-a51f-85df46403a8e'
uci set shadowsocksr.@servers[1].local_port='1234'
uci set shadowsocksr.@servers[1].security='auto'
uci set shadowsocksr.@servers[1].transport='tcp'
uci set shadowsocksr.@servers[1].tcp_guise='http'
uci set shadowsocksr.@servers[1].switch_enable='0'

uci commit shadowsocksr

# wifi
#uci set wireless.@wifi-device[0].disabled=0
#uci set wireless.@wifi-iface[0].ssid=Bruce-Net
#uci commit wireless

reboot
