```shell
# neo4j-etl
neo4j-etl generate-metadata-mapping --rdbms:url "jdbc:mysql://192.168.2.11:3306/cy_db?autoReconnect=true&useSSL=false&useCursorFetch=true&allowPublicKeyRetrieval=true" --rdbms:user admin --rdbms:password Czy.190815 --rdbms:schema cy_db --exclusion-mode-tables include --tables -g .*\.ent_.* --output-mapping-file /d/mysql_cy_db_mapping.json --debug

neo4j-etl export --rdbms:url "jdbc:mysql://192.168.2.11:3306/cy_db?autoReconnect=true&useSSL=false&useCursorFetch=true&allowPublicKeyRetrieval=true" --rdbms:user admin --rdbms:password Czy.190815 --neo4j:url "bolt://127.0.0.1:7687" --neo4j:user neo4j --neo4j:password Czy.190815 --using cypher:batch --unwind-batch-size 1000 --tx-batch-size 10000 --mapping-file /d/mysql_cy_db_mapping.json --csv-directory /d/Temp --debug

# get join cluster command
kubeadm token create --print-join-command

nmcli dev wifi connect XXXX password ****

mount -t nfs 192.168.1.3:/nfs_test /mnt/test1

# vmware RDM硬盘直通{0} 硬盘挂载地址, {1} 生成目标映射地址
vmkfstools -z /vmfs/devices/disks/t10.ATA_____ST4000NM000A2D2HZ100_________________________________WS213MF7 /vmfs/volumes/61900272-c8ccb923-7b10-7c10c91f7003/4T_1.vmdk
```