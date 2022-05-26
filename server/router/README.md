```shell
uci -f dhcp-domain -m import dhcp
uci show dhcp | grep '^dhcp.@domain\(.*\)=domain' | sed 's/=domain//' | xargs uci delete
```