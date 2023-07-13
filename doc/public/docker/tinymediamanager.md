# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.tinymediamanager.service: tinymediamanager
  traefik.http.services.tinymediamanager.loadbalancer.server.port: 4000

services:
  tinymediamanager:
    image: tinymediamanager/tinymediamanager:4.3.11.1
    container_name: tinymediamanager
    hostname: tinymediamanager
    labels:
      <<: *traefik-label
    volumes:
      - /volume1/storage/docker-data/tinymediamanager/data/:/data/
      - /volume1/public/media/:/media/
    expose:
      - "4000"
    restart: always
```