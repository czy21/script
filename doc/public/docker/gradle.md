
## docker-compose
```bash
docker-compose --project-name gradle --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.gradle-build-cache.service: gradle-build-cache
  traefik.http.services.gradle-build-cache.loadbalancer.server.port: 5071

services:

  gradle-build-cache:
    image: gradle/build-cache-node:14.0
    pull_policy: always
    container_name: gradle-build-cache
    hostname: gradle-build-cache
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "5071"
    volumes:
      - /volume5/storage/docker-data/gradle/data/cache/:/data/
    restart: always
```