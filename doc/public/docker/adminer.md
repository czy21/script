# dockerfile

# docker-compose
```shell
docker-compose --project-name adminer --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.adminer.service: adminer
  traefik.http.services.adminer.loadbalancer.server.port: 8080

services:

  adminer:
    image: adminer:4-standalone
    pull_policy: always
    container_name: adminer
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    restart: always
```