# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.phpldapadmin.service: phpldapadmin
  traefik.http.services.phpldapadmin.loadbalancer.server.port: 80

services:

  phpldapadmin:
    image: osixia/phpldapadmin:0.9.0
    pull_policy: always
    container_name: phpldapadmin
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "80"
    volumes:
      - "/volume1/storage/docker-data/phpldapadmin/conf/config.yaml:/container/environment/01-custom/env.yaml"
      - "/volume1/storage/docker-data/phpldapadmin/data/:/var/www/phpldapadmin/"
    restart: always
```