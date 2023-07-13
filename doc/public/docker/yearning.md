# dockerfile

# docker-compose
```yaml
version: '3.9'

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.yearning.service: yearning
  traefik.http.services.yearning.loadbalancer.server.port: 8000

services:
  yearning:
    image: chaiyd/yearning:v3.1.4-amd64
    pull_policy: always
    container_name: yearning
    labels:
      <<: *traefik-label
    expose:
      - "8000"
    environment:
      MYSQL_USER: <username>
      MYSQL_PASSWORD: <password>
      MYSQL_ADDR: <ip>
      MYSQL_DB: yearning
      SECRET_KEY: dbcjqheupqjsuwsm
      IS_DOCKER: is_docker
    command: /bin/bash -c "./Yearning install && ./Yearning run"
    restart: always
```