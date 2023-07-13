# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.zipkin.service: zipkin
  traefik.http.services.zipkin.loadbalancer.server.port: 9411

services:

  zipkin:
    image: openzipkin/zipkin:2.24
    pull_policy: always
    container_name: zipkin
    privileged: true
    user: root
    expose:
      - "9410"
      - "9411"
    labels:
      <<: *traefik-label
    restart: always
```