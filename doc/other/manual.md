# esxi 显卡直通后导致宿主机死机;解决方法
```shell
echo '10de ffff linke false' >> /etc/vmware/passthru.map
```

# vmware RDM硬盘直通{0} 硬盘挂载地址, {1} 生成目标映射地址
```shell
vmkfstools -z /vmfs/devices/disks/t10.ATA_____ST4000NM000A2D2HZ100_________________________________WS213MF7 /vmfs/volumes/ds15/4T_omv_1.vmdk
vmkfstools -z /vmfs/devices/disks/t10.ATA_____ST4000NM000A2D2HZ100_________________________________WS21R4S8 /vmfs/volumes/ds15/4T_dsm_1.vmdk
```

# 直通usb键鼠
```shell
# list usb device
lsusb
# vi /etc/vmware/config

usb.generic.allowHID = "TRUE"
usb.quirks.device0 = "0x1bcf:0x08b8 allow"
usb.quirks.device1 = "0x04d9:0x1702 allow"

# vi /bootbank/boot.cfg
CONFIG./USB/quirks=0x1bcf:0x08b8::0xffff:UQ_KBD_IGNORE:0x04d9:0x1702::0xffff:UQ_KBD_IGNORE
```