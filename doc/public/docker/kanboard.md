# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.kanboard.service: kanboard
  traefik.http.services.kanboard.loadbalancer.server.port: 80

services:

  kanboard:
    image: kanboard/kanboard:v1.2.25
    container_name: kanboard
    hostname: kanboard
    expose:
      - "80"
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    volumes:
      - /volume1/storage/docker-data/kanboard/data/data/:/var/www/app/data/
      - /volume1/storage/docker-data/kanboard/data/plugins/:/var/www/app/plugins/
      - /volume1/storage/docker-data/kanboard/data/ssl/:/etc/nginx/ssl/
    environment:
      DATABASE_URL: mysql://<username>:<password>@<ip>:3306/kanboard
      PLUGIN_INSTALLER: true
      LOG_DRIVER: stdout
      ENABLE_URL_REWRITE: false
    restart: always
```