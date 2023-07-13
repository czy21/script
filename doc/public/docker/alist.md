# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.alist.service: alist
  traefik.http.services.alist.loadbalancer.server.port: 5244

services:

  alist:
    image: xhofe/alist:v2.6.1
    container_name: alist
    labels:
      <<: *traefik-label
    privileged: true
    expose:
      - "5244"
    user: root
    volumes:
      - /volume1/storage/docker-data/alist/data/:/opt/alist/data/
    restart: always
```