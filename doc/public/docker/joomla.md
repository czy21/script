
## docker-compose
```bash
docker-compose --project-name joomla --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.joomla.service: joomla
  traefik.http.services.joomla.loadbalancer.server.port: 80

services:
  joomla:
    image: joomla:4.3.3-php8.0-apache
    container_name: joomla
    hostname: joomla
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "80"
    volumes:
      - /volume5/storage/docker-data/joomla/data/:/var/www/html
    environment:
      JOOMLA_DB_HOST: "<ip>"
      JOOMLA_DB_USER: "<username>"
      JOOMLA_DB_PASSWORD: "<password>"
      JOOMLA_DB_NAME: joomla
    restart: always
```