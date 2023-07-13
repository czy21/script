# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.heimdall.service: heimdall
  traefik.http.services.heimdall.loadbalancer.server.port: 80

services:

  heimdall:
    image: linuxserver/heimdall:2.5.2
    container_name: heimdall
    hostname: heimdall
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    volumes:
      - /volume1/storage/docker-data/heimdall/data/config/:/config/
    environment:
      PUID: 1000
      PGID: 1000
      TZ: Asia/Shanghai
    restart: always
```