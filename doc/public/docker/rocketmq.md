# dockerfile

# docker-compose
```yaml
version: "3.9"

x-rocketmq-common: &rocketmq-common
  image: apache/rocketmq:4.9.4
  privileged: true
  user: root
  restart: always

x-traefik-web-label: &traefik-web-label
  traefik.enable: true
  traefik.http.routers.rocketmq-web.service: rocketmq-web
  traefik.http.services.rocketmq-web.loadbalancer.server.port: 8080

services:
  rocketmq-setup:
    image: ubuntu:22.04
    container_name: rocketmq-setup
    volumes:
      - /volume1/storage/docker-data/rocketmq/conf/:/conf/
      - /volume1/storage/docker-data/rocketmq/broker/:/data/
    command: bash /conf/setup.sh
    restart: always
  rocketmq-namesrv:
    <<: *rocketmq-common
    container_name: rocketmq-namesrv
    ports:
      - "9876:9876"
    expose:
      - 9876
    volumes:
      - /volume1/storage/docker-data/rocketmq/namesrv/logs/:/logs/
    command: sh mqnamesrv
  rocketmq-broker-1:
    <<: *rocketmq-common
    container_name: rocketmq-broker-1
    hostname: rocketmq-broker-1
    expose:
      - 10909
      - 10911
      - 10912
    volumes:
      - /volume1/storage/docker-data/rocketmq/broker/1/logs/:/home/rocketmq/logs/
      - /volume1/storage/docker-data/rocketmq/broker/1/store/:/home/rocketmq/store/
      - /volume1/storage/docker-data/rocketmq/broker/:/data/
    command: sh mqbroker -n rocketmq-namesrv:9876 -c /data/1/broker.conf
    depends_on:
      - rocketmq-setup
      - rocketmq-namesrv
  rocketmq-broker-2:
    <<: *rocketmq-common
    container_name: rocketmq-broker-2
    hostname: rocketmq-broker-2
    expose:
      - 10909
      - 10911
      - 10912
    volumes:
      - /volume1/storage/docker-data/rocketmq/broker/2/logs/:/home/rocketmq/logs/
      - /volume1/storage/docker-data/rocketmq/broker/2/store/:/home/rocketmq/store/
      - /volume1/storage/docker-data/rocketmq/broker/:/data/
    command: sh mqbroker -n rocketmq-namesrv:9876 -c /data/2/broker.conf
    depends_on:
      - rocketmq-setup
      - rocketmq-namesrv
  rocketmq-dashboard:
    image: apacherocketmq/rocketmq-dashboard
    container_name: rocketmq-dashboard
    labels:
      <<: *traefik-web-label
    privileged: true
    user: root
    expose:
      - "8080"
    environment:
      JAVA_OPTS: -Drocketmq.namesrv.addr=rocketmq-namesrv:9876
    restart: always
```