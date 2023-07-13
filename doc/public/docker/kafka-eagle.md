# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.kafka-eagle.service: kafka-eagle
  traefik.http.services.kafka-eagle.loadbalancer.server.port: 8048

services:
  kafka-eagle:
    image: registry.czy21-internal.com/library/kafka-eagle
    pull_policy: always
    container_name: kafka-eagle
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "8048"
    volumes:
      - /volume1/storage/docker-data/kafka-eagle/conf/system-config.properties:/opt/kafka-eagle/conf/system-config.properties
      - /volume1/storage/docker-data/kafka-eagle/logs/:/opt/kafka-eagle/logs/
    restart: always
```