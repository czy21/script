# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.influxdb.service: influxdb
  traefik.http.services.influxdb.loadbalancer.server.port: 8086

services:

  influxdb:
    image: influxdb:2.6.1
    container_name: influxdb
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "8086"
    volumes:
      - /volume1/storage/docker-data/influxdb/conf/:/etc/influxdb2/
      - /volume1/storage/docker-data/influxdb/data/:/var/lib/influxdb2/
    environment:
      DOCKER_INFLUXDB_INIT_MODE: setup
      DOCKER_INFLUXDB_INIT_USERNAME: "<username>"
      DOCKER_INFLUXDB_INIT_PASSWORD: "<password>"
      DOCKER_INFLUXDB_INIT_ORG: "example"
      DOCKER_INFLUXDB_INIT_BUCKET: "default"
    restart: always
```