
## docker-compose
```bash
docker-compose --project-name jellyfin --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.jellyfin.service: jellyfin
  traefik.http.services.jellyfin.loadbalancer.server.port: 8096

services:
  jellyfin:
    image: linuxserver/jellyfin:10.8.10
    container_name: jellyfin
    hostname: jellyfin
    labels:
      <<: *traefik-label
    expose:
      - "8096"
    volumes:
      - /volume5/storage/docker-data/jellyfin/conf/:/config/
      - /volume5/public/media/:/media/
    environment:
      PUID: 1000
      PGID: 1000
      TZ: Asia/Shanghai
    devices:
      - /dev/dri:/dev/dri
```