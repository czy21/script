# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.taskcafe.service: taskcafe
  traefik.http.services.taskcafe.loadbalancer.server.port: 3333

services:

  taskcafe:
    image: taskcafe/taskcafe:0.3.6
    container_name: taskcafe
    hostname: taskcafe
    expose:
      - "3333"
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    volumes:
      - /volume1/storage/docker-data/taskcafe/data/:/data/
    environment:
      TASKCAFE_DATABASE_HOST: "<ip>"
      TASKCAFE_DATABASE_USER: "postgres"
      TASKCAFE_DATABASE_PASSWORD: "<password>"
      TASKCAFE_DATABASE_NAME: "taskcafe"
      TASKCAFE_MIGRATE: true
    restart: always
```