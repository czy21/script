```shell
docker run --rm --name pulsar-init apachepulsar/pulsar:2.10.0 bin/pulsar initialize-cluster-metadata \
  --cluster cluster1 \
  --zookeeper 192.168.2.18:2181,192.168.2.18:2182,192.168.2.18:2183/pulsar/cluster1 \
  --configuration-store 192.168.2.18:2181,192.168.2.18:2182,192.168.2.18:2183/pulsar/cluster1 \
  --web-service-url http://pulsar-proxy:8080 \
  --broker-service-url pulsar://pulsar-proxy:6650
```