# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.traefik.service: traefik
  traefik.http.services.traefik.loadbalancer.server.port: 8080

services:

  traefik:
    image: traefik:v2.10.1
    container_name: traefik
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "80"
      - "443"
      - "8080"
      - "8082"
    volumes:
      - /volume1/storage/docker-data/traefik/conf/traefik.yml:/etc/traefik/traefik.yml
      - /volume1/storage/docker-data/traefik/conf/conf.d/:/etc/traefik/conf.d/
      - /volume1/storage/docker-data/traefik/conf/cert/:/etc/traefik/cert/
      - /var/run/docker.sock:/var/run/docker.sock:ro
    restart: always
```