# dockerfile

# docker-compose
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
      KAFKA_SERVER_advertised.listeners: PLAINTEXT://<ip>:9092
      KAFKA_SERVER_zookeeper.connect: <ip>:2181,<ip>:2182,<ip>:2183/kafka/cluster1
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
      KAFKA_SERVER_advertised.listeners: PLAINTEXT://<ip>:9093
      KAFKA_SERVER_zookeeper.connect: <ip>:2181,<ip>:2182,<ip>:2183/kafka/cluster1
      KAFKA_SERVER_log.retention.hours: 720
      KAFKA_SERVER_log.roll.hours: 4
      KAFKA_SERVER_log.segment.bytes: 1073741824
    restart: always
```