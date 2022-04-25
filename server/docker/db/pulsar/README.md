```shell
docker run --rm --name pulsar-init apachepulsar/pulsar:2.10.0 bin/pulsar initialize-cluster-metadata \
  --cluster cluster1 \
  --zookeeper 192.168.2.18:2181,192.168.2.18:2182,192.168.2.18:2183/pulsar/cluster1 \
  --configuration-store 192.168.2.18:2181,192.168.2.18:2182,192.168.2.18:2183/pulsar/cluster1 \
  --web-service-url http://pulsar-broker1:8080,pulsar-broker2:8080 \
  --broker-service-url pulsar://pulsar-broker1:6650,pulsar-broker2:6650
```