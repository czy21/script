# dockerfile

# docker-compose
```yaml
version: "3.9"

x-redis-common: &redis-common
  image: redis/redis-stack-server:6.2.4-v3
  privileged: true
  user: root
  environment:
    TZ: Asia/Shanghai
  restart: always

x-traefik-exporter-label: &traefik-exporter-label
  traefik.enable: true
  traefik.http.routers.redis-exporter.service: redis-exporter
  traefik.http.services.redis-exporter.loadbalancer.server.port: 9121

services:
  redis-1:
    <<: *redis-common
    container_name: redis-1
    ports:
      - "7000:7000"
      - "17000:17000"
    volumes:
      - /volume1/storage/docker-data/redis/data/1/:/data/
    environment:
      REDIS_ARGS: |-
        --port 7000
        --requirepass <password>
        --appendonly yes
        --cluster-enabled yes
        --cluster-announce-ip <ip>
  redis-2:
    <<: *redis-common
    container_name: redis-2
    ports:
      - "7001:7001"
      - "17001:17001"
    volumes:
      - /volume1/storage/docker-data/redis/data/2/:/data/
    environment:
      REDIS_ARGS: |-
        --port 7001
        --requirepass <password>
        --appendonly yes
        --cluster-enabled yes
        --cluster-announce-ip <ip>
  redis-3:
    <<: *redis-common
    container_name: redis-3
    ports:
      - "7002:7002"
      - "17002:17002"
    volumes:
      - /volume1/storage/docker-data/redis/data/3/:/data/
    environment:
      REDIS_ARGS: |-
        --port 7002
        --requirepass <password>
        --appendonly yes
        --cluster-enabled yes
        --cluster-announce-ip <ip>
  redis-exporter-7000:
    image: oliver006/redis_exporter:alpine
    labels:
      <<: *traefik-exporter-label
    container_name: redis-exporter-7000
    user: root
    expose:
      - "9121"
    command:
      - --redis.addr=redis://redis-1:7000
      - --redis.password=<password>
    environment:
      REDIS_EXPORTER_IS_CLUSTER: "true"
    restart: always
```