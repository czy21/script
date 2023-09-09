```shell
# neo4j-etl
neo4j-etl generate-metadata-mapping --rdbms:url "jdbc:mysql://192.168.2.11:3306/cy_db?autoReconnect=true&useSSL=false&useCursorFetch=true&allowPublicKeyRetrieval=true" --rdbms:user admin --rdbms:password ***REMOVED*** --rdbms:schema cy_db --exclusion-mode-tables include --tables -g .*\.ent_.* --output-mapping-file /d/mysql_cy_db_mapping.json --debug

neo4j-etl export --rdbms:url "jdbc:mysql://192.168.2.11:3306/cy_db?autoReconnect=true&useSSL=false&useCursorFetch=true&allowPublicKeyRetrieval=true" --rdbms:user admin --rdbms:password ***REMOVED*** --neo4j:url "bolt://127.0.0.1:7687" --neo4j:user neo4j --neo4j:password ***REMOVED*** --using cypher:batch --unwind-batch-size 1000 --tx-batch-size 10000 --mapping-file /d/mysql_cy_db_mapping.json --csv-directory /d/Temp --debug

# get join cluster command
kubeadm token create --print-join-command

nmcli dev wifi connect XXXX password ****

mount -t nfs 192.168.1.3:/nfs_test /mnt/test1

# vmware RDM硬盘直通{0} 硬盘挂载地址, {1} 生成目标映射地址
vmkfstools -z /vmfs/devices/disks/t10.ATA_____ST4000NM000A2D2HZ100_________________________________WS213MF7 /vmfs/volumes/ds15/4T_1.vmdk
vmkfstools -z /vmfs/devices/disks/t10.ATA_____ST4000NM000A2D2HZ100_________________________________WS21R4S8 /vmfs/volumes/ds15/4T_2.vmdk
vmkfstools -z /vmfs/devices/disks/t10.ATA_____Samsung_SSD_850_EVO_250GB_______________S2R7NX0K172814Y_____  /vmfs/volumes/ds15/SSD_250G_1.vmdk
vmkfstools -z /vmfs/devices/disks/t10.NVMe____Samsung_SSD_970_EVO_Plus_250GB__________C2659E1151382500  /vmfs/volumes/ds15/SSD_250G_2.vmdk

# vmware import ssl cert
cd /etc/vmware/ssl
mv rui.crt rui.crt.bak && mv rui.key rui.key.bak
scp rui.* <host>:/etc/vmware/ssl/
/etc/init.d/hostd restart && /etc/init.d/vpxa restart
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