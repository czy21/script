```shell
# ubuntu 22.04
sudo apt install -y build-essential clang flex g++ gawk gcc-multilib gettext git libncurses5-dev libssl-dev python3-distutils rsync unzip zlib1g-dev qemu-utils file
echo "
src-git plugin http://gitea.cluster.com/czyhome/openwrt-plugin.git
#src-link plugin /volume2/openwrt-plugin
" >> feeds.conf.default

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

```shell
luci-app-dawn           # 分布式AP管理程序
luci-app-diag-core      # core诊断工具
luci-app-minidlna       # 多媒体共享
luci-app-mjpg-streamer  # 摄像头采集
luci-app-mosquitto      # MQTT 消息队列
luci-app-mwan3          # 多播负载均衡
luci-app-nlbwmon        # 网络带宽监视器
luci-app-nut            # ups 管理
luci-app-ocserv         # OpenConnect VPN服务
luci-app-openwisp       # AP管理
luci-app-opkg           
luci-app-radicale2      # 日历 联系人同步
luci-app-ksmbd          # smb server 
luci-app-nfs            # nfs server
```