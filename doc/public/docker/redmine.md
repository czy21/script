# dockerfile

# docker-compose
```shell
docker-compose --project-name redmine --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.redmine.service: redmine
  traefik.http.services.redmine.loadbalancer.server.port: 3000

services:

  redmine:
    image: redmine:5.0.2-bullseye
    container_name: redmine
    labels:
      <<: *traefik-label
    expose:
      - "3000"
    volumes:
      - /volume1/storage/docker-data/redmine/data/files/:/usr/src/redmine/files/
    environment:
      REDMINE_DB_MYSQL: '192.168.2.18'
      REDMINE_DB_USERNAME: 'admin'
      REDMINE_DB_PASSWORD: '***REMOVED***'
      REDMINE_DB_DATABASE: 'redmine'
      REDMINE_DB_ENCODING: 'utf8'
```