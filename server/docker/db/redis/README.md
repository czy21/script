# create cluster
```shell
redis-cli --cluster create 192.168.2.18:7000 192.168.2.18:7001 192.168.2.18:7002 --cluster-replicas 0 -a <password>
```