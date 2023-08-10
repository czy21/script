
## docker-compose
```bash
docker-compose --project-name drupal --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.drupal.service: drupal
  traefik.http.services.drupal.loadbalancer.server.port: 80

services:
  drupal:
    image: drupal:9.5.10-php8.1-apache-bullseye
    container_name: drupal
    hostname: drupal
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "80"
    restart: always
```