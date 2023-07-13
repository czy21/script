# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.ndisk.service: ndisk
  traefik.http.services.ndisk.loadbalancer.server.port: 8080

services:

  ndisk:
    image: registry.czy21-internal.com/library/ndisk:latest
    pull_policy: always
    container_name: ndisk
    labels:
      <<: *traefik-label
    expose:
      - "8080"
    volumes:
      - /volume1/storage/docker-data/ndisk/conf/app.yaml:/app/app.yaml
      - /volume1/storage/docker-data/ndisk/data/:/data/
    environment:
      CONFIG_FILE: /app/app.yaml
    restart: always
```