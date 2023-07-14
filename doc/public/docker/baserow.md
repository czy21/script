# dockerfile

# docker-compose
```shell
docker-compose --project-name baserow --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.baserow.service: baserow
  traefik.http.services.baserow.loadbalancer.server.port: 80

services:
  baserow:
    image: baserow/baserow:1.18.0
    container_name: baserow
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "80"
      - "443"
    volumes:
      - /volume1/storage/docker-data/baserow/data/:/baserow/data/
    environment:
      BASEROW_PUBLIC_URL: http://baserow.czy21-internal.com
      REDIS_URL: redis://:***REMOVED***@192.168.2.2:6379
      DATABASE_URL: postgresql://postgres:***REMOVED***@192.168.2.18:5432/baserow
    restart: always
```