```shell
docker run --rm --name pulsar-init apachepulsar/pulsar:2.9.2 bin/pulsar initialize-cluster-metadata \
  --cluster pulsar \
  --zookeeper 192.168.2.18:2181/pulsar/cluster1 \
  --configuration-store 192.168.2.18:2181/pulsar/cluster1 \
  --web-service-url http://pulsar-proxy:8080 \
  --broker-service-url pulsar://pulsar-proxy:6650
```