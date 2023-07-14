# dockerfile

# docker-compose
```shell
docker-compose --project-name archery --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.archery.service: archery
  traefik.http.services.archery.loadbalancer.server.port: 9123

services:

  archery:
    image: hhyo/archery:v1.9.1
    container_name: archery
    labels:
      <<: *traefik-label
    privileged: true
    expose:
      - "9123"
    user: root
    volumes:
      - /volume1/storage/docker-data/archery/data/:/data/
    environment:
      NGINX_PORT: "9123"
      DEBUG: false
      DATABASE_URL: mysql://admin:***REMOVED***@192.168.2.18:3306/archery
      CACHE_URL: redis://192.168.2.2:6379/0?PASSWORD=***REMOVED***
      CSRF_TRUSTED_ORIGINS: http://127.0.0.1:9123
      ENABLE_LDAP: false
    restart: always
```