```shell
#build guide: https://openwrt.org/docs/guide-developer/toolchain/use-buildsystem

# convert
gunzip openwrt-x86-64-generic-squashfs-combined-efi.img.gz
qemu-img convert -f raw -O vmdk openwrt-x86-64-generic-squashfs-combined-efi.img openwrt-x86-64-generic-squashfs-combined-efi.vmdk;
```