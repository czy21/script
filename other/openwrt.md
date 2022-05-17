```shell
#build guide: https://openwrt.org/docs/guide-developer/toolchain/use-buildsystem

# luci required
# Luci -> Modules -> luci-compat

# feeds
for i in "luci-app-vlmcsd" "luci-app-softethervpn"; do \
  svn checkout "https://github.com/coolsnowwolf/luci/trunk/applications/$i" "feeds/luci/applications/$i"; \
done

for i in "vlmcsd"; do \
  svn checkout "https://github.com/coolsnowwolf/packages/trunk/net/$i" "feeds/packages/net/$i"; \
done

mkdir -p package/lean/
for i in "ddns-scripts_aliyun"; do \
  svn checkout "https://github.com/coolsnowwolf/lede/trunk/package/lean/$i" "package/lean/$i"; \
done

# helloworld
# ignore Base System -> dnsmasq

# convert
projectRoot=/home/bruce/openwrt/bin/targets/x86/64/openwrt-x86-64-generic-squashfs-combined-efi; \
gunzip --keep --force ${projectRoot}.img.gz; \
qemu-img convert -f raw -O vmdk ${projectRoot}.img ${projectRoot}.vmdk
```

https://github.com/immortalwrt/packages/trunk/net/