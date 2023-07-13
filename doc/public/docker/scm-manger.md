# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.scm-manger.service: scm-manger
  traefik.http.services.scm-manger.loadbalancer.server.port: 8080

services:
  scm-manager:
    image: scmmanager/scm-manager:2.37.0-debian
    container_name: scm-manager
    labels:
      <<: *traefik-label
    privileged: true
    expose:
      - "8080"
      - "22"
    user: root
    volumes:
      - /volume1/storage/docker-data/scm-manger/data/:/var/lib/scm/
    environment:
      JAVA_OPTS: "-Dscm.initialUser=<username> -Dscm.initialPassword=<password>"
```