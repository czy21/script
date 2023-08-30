```bash
#build guide: https://openwrt.org/docs/guide-developer/toolchain/use-buildsystem
sed -i -e 's|https://git.openwrt.org/\(.*\)/|http://gitea.czy21-internal.com/openwrt/|g' -e 's|\^.*|;openwrt-22.03|' feeds.conf.default

# convert
ssh ubun \
'
projectRoot=openwrt/bin/targets/x86/64/openwrt-x86-64-generic-squashfs-combined-efi;
gunzip --keep --force ${projectRoot}.img.gz;
qemu-img convert -f raw -O vmdk ${projectRoot}.img ${projectRoot}.vmdk
'

# repair
vmkfstools -x check <>.vmdk

vmkfstools -x repair <>.vmdk
```