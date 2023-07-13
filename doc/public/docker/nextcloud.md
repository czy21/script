# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.nextcloud.service: nextcloud
  traefik.http.services.nextcloud.loadbalancer.server.port: 80

services:
  nextcloud:
    image: nextcloud:24.0.2
    container_name: nextcloud
    labels:
      <<: *traefik-label
    privileged: true
    expose:
      - "80"
    volumes:
      - /volume1/storage/docker-data/nextcloud/data/:/var/www/html
    environment:
      NEXTCLOUD_ADMIN_USER: 'admin'
      NEXTCLOUD_ADMIN_PASSWORD: '***REMOVED***'
```