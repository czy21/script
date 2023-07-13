# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.go-pulsar-manager.service: go-pulsar-manager
  traefik.http.services.go-pulsar-manager.loadbalancer.server.port: 3000

services:

  go-pulsar-manager:
    image: registry.czy21-internal.com/library/go-pulsar-manager:master
    container_name: go-pulsar-manager
    labels:
      <<: *traefik-label
    privileged: true
    expose:
      - "3000"
      - "8080"
    user: root
    volumes:
      - /volume1/storage/docker-data/go-pulsar-manager/conf/app.yaml:/app/app.yaml
      - /volume1/storage/docker-data/go-pulsar-manager/log/:/app/log/
    environment:
      TZ: Asia/Shanghai
      GIN_MODE: release
      GPM_CONFIG_FILE: /app/app.yaml


```