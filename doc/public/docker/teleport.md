# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.teleport.service: teleport
  traefik.http.services.teleport.loadbalancer.server.port: 80

services:
  teleport:
    image: public.ecr.aws/gravitational/teleport-lab:10
    container_name: teleport
    hostname: teleport
    labels:
      <<: *traefik-label
    entrypoint: /bin/sh
    command: -c "/usr/bin/dumb-init teleport start -d -c /etc/teleport.d/teleport.yaml --insecure --insecure-no-tls"
    expose:
      - "80"
    volumes:
      - /volume1/storage/docker-data/teleport/data/empty/:/teleport/
      - /volume1/storage/docker-data/teleport/conf/teleport.yaml:/etc/teleport.d/teleport.yaml
      - /volume1/storage/docker-data/teleport/data/data/:/var/lib/teleport
```