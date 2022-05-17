```shell
#build guide: https://openwrt.org/docs/guide-developer/toolchain/use-buildsystem

# luci required
# Luci -> Modules -> luci-compat

# helloworld
# ignore Base System -> dnsmasq

# convert
projectRoot=/home/bruce/openwrt/bin/targets/x86/64/openwrt-x86-64-generic-squashfs-combined-efi; \
gunzip --keep --force ${projectRoot}.img.gz; \
qemu-img convert -f raw -O vmdk ${projectRoot}.img ${projectRoot}.vmdk
```

https://github.com/immortalwrt/packages/trunk/net/