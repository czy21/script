```shell
#build guide: https://openwrt.org/docs/guide-developer/toolchain/use-buildsystem

# luci required
# Luci -> Modules -> luci-compat

# feeds
for i in "luci-app-vlmcsd"; do \
  svn checkout "https://github.com/coolsnowwolf/luci/trunk/applications/$i" "feeds/luci/applications/$i"; \
done

for i in "vlmcsd"; do \
  svn checkout "https://github.com/coolsnowwolf/packages/trunk/net/$i" "feeds/packages/net/$i"; \
done

# helloworld
# ignore Base System -> dnsmasq

# convert
projectRoot=/home/bruce/openwrt/bin/targets/x86/64;
gunzip --keep --force ${projectRoot}/openwrt-x86-64-generic-squashfs-combined-efi.img.gz;
qemu-img convert -f raw -O vmdk ${projectRoot}/openwrt-x86-64-generic-squashfs-combined-efi.img ${projectRoot}/openwrt-x86-64-generic-squashfs-combined-efi.vmdk
```

https://github.com/immortalwrt/packages/trunk/net/