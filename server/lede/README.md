```shell
git clone https://github.com/coolsnowwolf/lede

echo 'src-git helloworld https://github.com/fw876/helloworld' >> feeds.conf.default
./scripts/feeds update -a && ./scripts/feeds install -a
rm -rf ./tmp && rm -rf .config
make menuconfig
make -j8 download V=s
# single thread
nohup make -j1 V=s &
# multi thread
nohup make -j$(($(nproc) + 1)) V=s &
```

```shell
uci -f dhcp-domain -m import dhcp

uci show dhcp | grep '^dhcp.@domain\(.*\)=domain' | sed 's/=domain//' | xargs uci delete
```

```shell
Target System: Broadcom BCM27xx
Target Images 
  Root filesystem partition size
Kernel modules > USB Support:
  kmod-usb-dwc2
  kmod-usb-net-cdc-ether
```