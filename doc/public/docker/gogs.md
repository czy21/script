# dockerfile

# docker-compose
```shell
docker-compose --project-name gogs --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.gogs.service: gogs
  traefik.http.services.gogs.loadbalancer.server.port: 3000

services:

  gogs:
    image: gogs/gogs
    container_name: gogs
    labels:
      <<: *traefik-label
    privileged: true
    expose:
      - "3000"
      - "22"
    user: root
    volumes:
      - /volume1/storage/docker-data/gogs/data/:/data/
      - /volume1/storage/docker-data/gogs/backup/:/backup/


```