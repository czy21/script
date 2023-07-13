# dockerfile

# docker-compose
```yaml
version: "3.9"

x-pulsar-common: &pulsar-common
  image: apachepulsar/pulsar:2.9.2
  privileged: true
  user: root


x-traefik-pulsar-proxy-label: &traefik-pulsar-proxy-label
  traefik.enable: true
  traefik.http.routers.pulsar-proxy.service: pulsar-proxy
  traefik.http.services.pulsar-proxy.loadbalancer.server.port: 8080

services:
  
  pulsar-bookie1:
    <<: *pulsar-common
    container_name: pulsar-bookie1
    hostname: pulsar-bookie1
    expose:
      - "3181"
    volumes:
      - /volume1/storage/docker-data/pulsar/conf/bookie.conf:/pulsar/conf/bookkeeper.conf
      - /volume1/storage/docker-data/pulsar/data/bookie/1/:/pulsar/data/bookie/
      - /volume1/storage/docker-data/pulsar/log/bookie/1/:/pulsar/logs/
    command: bin/pulsar bookie
    environment:
      PULSAR_MEM: "-Xms128m -Xmx256m -XX:MaxDirectMemorySize=256m"
  
  pulsar-bookie2:
    <<: *pulsar-common
    container_name: pulsar-bookie2
    hostname: pulsar-bookie2
    expose:
      - "3181"
    volumes:
      - /volume1/storage/docker-data/pulsar/conf/bookie.conf:/pulsar/conf/bookkeeper.conf
      - /volume1/storage/docker-data/pulsar/data/bookie/2/:/pulsar/data/bookie/
      - /volume1/storage/docker-data/pulsar/log/bookie/2/:/pulsar/logs/
    command: bin/pulsar bookie
    environment:
      PULSAR_MEM: "-Xms128m -Xmx256m -XX:MaxDirectMemorySize=256m"
  
  
  pulsar-broker1:
    <<: *pulsar-common
    container_name: pulsar-broker1
    hostname: pulsar-broker1
    expose:
      - "8080"
      - "6650"
    volumes:
      - /volume1/storage/docker-data/pulsar/conf/broker.conf:/pulsar/conf/broker.conf
      - /volume1/storage/docker-data/pulsar/log/broker/1/:/pulsar/logs/
    command: bin/pulsar broker
    environment:
      PULSAR_MEM: "-Xms128m -Xmx256m -XX:MaxDirectMemorySize=256m"
  
  pulsar-broker2:
    <<: *pulsar-common
    container_name: pulsar-broker2
    hostname: pulsar-broker2
    expose:
      - "8080"
      - "6650"
    volumes:
      - /volume1/storage/docker-data/pulsar/conf/broker.conf:/pulsar/conf/broker.conf
      - /volume1/storage/docker-data/pulsar/log/broker/2/:/pulsar/logs/
    command: bin/pulsar broker
    environment:
      PULSAR_MEM: "-Xms128m -Xmx256m -XX:MaxDirectMemorySize=256m"
  

  pulsar-proxy:
    <<: *pulsar-common
    container_name: pulsar-proxy
    hostname: pulsar-proxy
    labels:
      <<: *traefik-pulsar-proxy-label
    expose:
      - "8080"
      - "6650"
    ports:
      - "6650:6650"
    volumes:
      - /volume1/storage/docker-data/pulsar/conf/proxy.conf:/pulsar/conf/proxy.conf
      - /volume1/storage/docker-data/pulsar/log/proxy/:/pulsar/logs/
    command: bin/pulsar proxy
    environment:
      PULSAR_MEM: "-Xms64m -Xmx64m -XX:MaxDirectMemorySize=64m"
```