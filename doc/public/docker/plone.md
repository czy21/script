
## docker-compose
```bash
docker-compose --project-name plone --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.plone.service: plone
  traefik.http.services.plone.loadbalancer.server.port: 8080

services:
  plone:
    image: plone:5.2.7
    container_name: plone
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "8080"
    volumes:
      - /volume5/storage/docker-data/plone/data/:/data/
```