
## docker-compose
```bash
docker-compose --project-name piwigo --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: '3.9'

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.piwigo.service: piwigo
  traefik.http.services.piwigo.loadbalancer.server.port: 80

services:
  piwigo:
    image: linuxserver/piwigo
    container_name: piwigo
    labels:
      <<: *traefik-label
    expose:
      - "80"
    volumes:
      - /volume5/storage/docker-data/piwigo/conf/:/config/
      - /volume5/storage/docker-data/piwigo/data/:/gallery/
    environment:
      TZ: Asia/Shanghai
      PUID: 1000
      PGID: 1000

```