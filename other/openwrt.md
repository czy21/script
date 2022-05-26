```shell
echo 'src-git helloworld https://github.com/fw876/helloworld' >> feeds.conf.default
rm -rf ./tmp && rm -rf .config
./scripts/feeds update -a && ./scripts/feeds install -a
pkgName=plugin && ./scripts/feeds update ${pkgName} && ./scripts/feeds install -a -p ${pkgName}
make menuconfig
make -j8 download V=s
# single thread
nohup make -j1 V=s &
# multi thread
nohup make -j$(($(nproc) + 1)) V=s &
```
```shell
# pip repo
~/.pip/pip.conf
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
```
```bash
#build guide: https://openwrt.org/docs/guide-developer/toolchain/use-buildsystem
sed -i 's|https://git.openwrt.org/\(.*\)/|http://gitea.cluster.com/openwrt/|g' feeds.conf.default
# select luci-app-bundle-server

# helloworld
# ignore Base System -> dnsmasq

# convert
ssh ubun \
'
projectRoot=openwrt/bin/targets/x86/64/openwrt-x86-64-generic-squashfs-combined-efi;
gunzip --keep --force ${projectRoot}.img.gz;
qemu-img convert -f raw -O vmdk ${projectRoot}.img ${projectRoot}.vmdk
' && \
scp ubun:openwrt/bin/targets/x86/64/openwrt-x86-64-generic-squashfs-combined-efi.vmdk .

# set vmdk size
image_name=openwrt-x86-64-generic-squashfs-combined-efi; \
esxi_image_dir=/vmfs/volumes/datastore1/image; \
scp ${image_name}.vmdk esxi1:${esxi_image_dir}/ && \
ssh esxi1 "vmkfstools -X 500M ${esxi_image_dir}/${image_name}.vmdk" && \
scp esxi1:${esxi_image_dir}/${image_name}.vmdk . && scp esxi1:${esxi_image_dir}/${image_name}-s001.vmdk .

# repair
vmkfstools -x check <>.vmdk

vmkfstools -x repair <>.vmdk
```

## raspberry pi zero w
```bash
Target System: Broadcom BCM27xx
Target Images 
  Root filesystem partition size
Kernel modules > USB Support:
  kmod-usb-dwc2
  kmod-usb-net-cdc-ether
```