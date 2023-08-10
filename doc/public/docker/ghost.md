
## docker-compose
```bash
docker-compose --project-name ghost --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.ghost.service: ghost
  traefik.http.services.ghost.loadbalancer.server.port: 2368

services:
  ghost:
    image: ghost:5.58.0
    container_name: ghost
    hostname: ghost
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "2368"
    volumes:
      - /volume5/storage/docker-data/ghost/data/:/var/lib/ghost/content/
    environment:
      database__client: mysql
      database__connection__host: "<ip>"
      database__connection__user: "<username>"
      database__connection__password: "<password>"
      database__connection__database: ghost
    restart: always
```