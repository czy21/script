```shell
#build guide: https://openwrt.org/docs/guide-developer/toolchain/use-buildsystem

# luci required
# Luci -> Modules -> luci-compat

# 

# helloworld
# ignore Base System -> dnsmasq

# convert

ssh ubun \
'
projectRoot=openwrt/bin/targets/x86/64/openwrt-x86-64-generic-ext4-combined-efi;
gunzip --keep --force ${projectRoot}.img.gz;
qemu-img convert -f raw -O vmdk ${projectRoot}.img ${projectRoot}.vmdk
'
scp ubun:openwrt/bin/targets/x86/64/openwrt-x86-64-generic-ext4-combined-efi.vmdk .

# set vmdk size
scp openwrt-x86-64-generic-ext4-combined-efi.vmdk esxi1:/vmfs/volumes/datastore1/openwrt-dev/
# esxi reboot disk exception resolve
ssh esxi1 'vmkfstools -X 1G /vmfs/volumes/datastore1/openwrt-dev/openwrt-x86-64-generic-ext4-combined-efi.vmdk'
scp esxi1:/vmfs/volumes/datastore1/openwrt-dev/openwrt-x86-64-generic-ext4-combined-efi.vmdk . 
```