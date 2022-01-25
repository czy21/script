# create cluster
```shell
redis-cli --cluster create 192.168.2.18:7001 192.168.2.18:7002 192.168.2.18:7003 --cluster-replicas 0 -a '<password>'
```