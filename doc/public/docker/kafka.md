
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/kafka --file Dockerfile . --pull
```
```dockerfile
FROM openjdk:11-jdk

ENV KAFKA_VERSION=2.13-3.4.0
ENV KAFKA_TGZ_URL=https://downloads.apache.org/kafka/3.4.0/kafka_${KAFKA_VERSION}.tgz
ENV KAFKA_HOME=/opt/kafka
ENV PATH=$KAFKA_HOME/bin:$PATH

RUN mkdir -p $KAFKA_HOME
#COPY ___temp/kafka_${KAFKA_VERSION}.tgz $KAFKA_HOME/src.tgz
RUN wget -nv -O $KAFKA_HOME/src.tgz $KAFKA_TGZ_URL;
RUN tar -xf $KAFKA_HOME/src.tgz --strip-components=1 -C $KAFKA_HOME && rm $KAFKA_HOME/src.tgz && chown -R root:root $KAFKA_HOME
RUN rm -rf $KAFKA_HOME/site-docs

WORKDIR $KAFKA_HOME

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["/logs"]
ENTRYPOINT ["/docker-entrypoint.sh"]
```
## docker-compose
```bash
docker-compose --project-name kafka --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:
  kafka-1:
    image: docker.io/czy21/kafka
    pull_policy: always
    container_name: kafka-1
    privileged: true
    user: root
    ports:
      - "9092:9092"
      - "9999:9999"
    volumes:
      - /volume5/storage/docker-data/kafka/logs/1:/logs/
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
    image: docker.io/czy21/kafka
    pull_policy: always
    container_name: kafka-2
    privileged: true
    user: root
    ports:
      - "9093:9093"
      - "10000:10000"
    volumes:
      - /volume5/storage/docker-data/kafka/logs/2:/logs/
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