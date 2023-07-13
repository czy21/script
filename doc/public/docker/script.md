# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.script.service: script
  traefik.http.services.script.loadbalancer.server.port: 80

services:

  script:
    image: registry.czy21-internal.com/library/script:master
    pull_policy: always
    container_name: script
    labels:
      <<: *traefik-label
    expose:
      - "80"
    restart: always
```