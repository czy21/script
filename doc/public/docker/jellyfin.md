
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
    image: jellyfin/jellyfin
    container_name: jellyfin
    labels:
      <<: *traefik-label
    expose:
      - "8096"
    volumes:
      - /volume5/storage/docker-data/jellyfin/conf/:/config/
      - /volume5/storage/docker-data/jellyfin/data/cache/:/cache/
      - /volume5/public/media/:/media/
    devices:
      - /dev/dri:/dev/dri

```