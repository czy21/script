
## docker-compose
```bash
docker-compose --project-name mix --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.mix.service: mix
  traefik.http.services.mix.loadbalancer.server.port: 80

services:
  mix:
    image: mixcore/mix.core
    container_name: mix
    hostname: mix
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "80"
    restart: always
```