# dockerfile

# docker-compose
```shell
docker-compose --project-name focalboard --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.focalboard.service: focalboard
  traefik.http.services.focalboard.loadbalancer.server.port: 8000

services:

  focalboard:
    image: mattermost/focalboard:7.5.2
    container_name: focalboard
    hostname: focalboard
    expose:
      - "8000"
      - "9092"
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    volumes:
      - /volume5/storage/docker-data/focalboard/data/:/data/
    restart: always
```