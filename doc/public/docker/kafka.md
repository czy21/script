# dockerfile

# docker-compose
```shell
docker-compose --project-name kafka --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:
  kafka-1:
    image: registry.czy21-internal.com/library/kafka
    pull_policy: always
    container_name: kafka-1
    privileged: true
    user: root
    ports:
      - "9092:9092"
      - "9999:9999"
    volumes:
      - /volume1/storage/docker-data/kafka/logs/1:/logs/
    environment:
      JMX_PORT: 9999
      KAFKA_HEAP_OPTS: -Xms256M -Xmx512M
      KAFKA_SERVER_broker.id: 1
      KAFKA_SERVER_listeners: PLAINTEXT://kafka-1:9092
      KAFKA_SERVER_advertised.listeners: PLAINTEXT://192.168.2.18:9092
      KAFKA_SERVER_zookeeper.connect: 192.168.2.18:2181,192.168.2.18:2182,192.168.2.18:2183/kafka/cluster1
      KAFKA_SERVER_log.retention.hours: 720
      KAFKA_SERVER_log.roll.hours: 4
      KAFKA_SERVER_log.segment.bytes: 1073741824
    restart: always
  kafka-2:
    image: registry.czy21-internal.com/library/kafka
    pull_policy: always
    container_name: kafka-2
    privileged: true
    user: root
    ports:
      - "9093:9093"
      - "10000:10000"
    volumes:
      - /volume1/storage/docker-data/kafka/logs/2:/logs/
    environment:
      JMX_PORT: 10000
      KAFKA_HEAP_OPTS: -Xms256M -Xmx512M
      KAFKA_SERVER_broker.id: 2
      KAFKA_SERVER_listeners: PLAINTEXT://kafka-2:9093
      KAFKA_SERVER_advertised.listeners: PLAINTEXT://192.168.2.18:9093
      KAFKA_SERVER_zookeeper.connect: 192.168.2.18:2181,192.168.2.18:2182,192.168.2.18:2183/kafka/cluster1
      KAFKA_SERVER_log.retention.hours: 720
      KAFKA_SERVER_log.roll.hours: 4
      KAFKA_SERVER_log.segment.bytes: 1073741824
    restart: always
```