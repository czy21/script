```bash
#build guide: https://openwrt.org/docs/guide-developer/toolchain/use-buildsystem
sed -i 's|https://git.openwrt.org/\(.*\)/|http://gitea.czy21-internal.com/openwrt/|g' feeds.conf.default

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
# cron.err xxxxxx 意为cron执行过任务,不是任务内部出错

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