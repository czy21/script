# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.dbeaver.service: dbeaver
  traefik.http.services.dbeaver.loadbalancer.server.port: 8978

services:
  dbeaver:
    image: dbeaver/cloudbeaver:23.1.1
    container_name: dbeaver
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "8978"
    volumes:
      - /volume1/storage/docker-data/dbeaver/data/:/opt/cloudbeaver/workspace/
    restart: always
```