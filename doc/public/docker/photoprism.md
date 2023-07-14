
## docker-compose
```bash
docker-compose --project-name photoprism --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: '3.9'

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.photoprism.service: photoprism
  traefik.http.services.photoprism.loadbalancer.server.port: 2342

services:
  photoprism:
    image: photoprism/photoprism:220617-bullseye
    container_name: photoprism
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "2342"
    volumes:
      - /volume5/storage/docker-data/photoprism/data/:/photoprism
    restart: always
    environment:
      PHOTOPRISM_ADMIN_PASSWORD: "<password>"
```