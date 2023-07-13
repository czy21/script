# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.emby.service: emby
  traefik.http.services.emby.loadbalancer.server.port: 8096

services:
  emby:
    image: emby/embyserver:4.8.0.39
    container_name: emby
    hostname: emby
    labels:
      <<: *traefik-label
    expose:
      - "8096"
      - "8920"
    volumes:
      - /volume1/storage/docker-data/emby/data/:/config/
      - /volume1/public/media/:/media/
    environment:
      - UID=1000
      - GID=1000
      - GIDLIST=1000
    devices:
      - /dev/dri:/dev/dri
    restart: always
```