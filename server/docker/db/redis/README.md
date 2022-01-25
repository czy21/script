# create cluster
```shell
redis-cli --cluster create 192.168.2.18:6379 192.168.2.18:6380 192.168.2.18:6381 --cluster-replicas 0 -a '<password>'
```