# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.demo-portal-java.rule: Host(`demo-portal-java.czy21-internal.com`)
  traefik.http.routers.demo-portal-java.service: demo-portal-java
  traefik.http.services.demo-portal-java.loadbalancer.server.port: 8080

services:
  demo-portal-java:
    image: registry.czy21-internal.com/library/demo-portal:master
    pull_policy: always
    labels:
      <<: *traefik-label
    container_name: demo-portal-java
    pull_policy: always
    privileged: true
    volumes:
      - /volume1/storage/docker-data/demo-portal-java/conf/:/app/conf/
      - /volume1/storage/docker-data/demo-portal-java/data/:/app/data/
    environment:
      APP_ARGS: -Xms128m -Xmx512m -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=256m
```