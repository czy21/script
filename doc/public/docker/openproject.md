# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.openproject.service: openproject
  traefik.http.services.openproject.loadbalancer.server.port: 80

services:

  op-app:
    image: openproject/community:12.3.3
    container_name: op-app
    hostname: op-app
    expose:
      - "80"
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    volumes:
      - /volume1/storage/docker-data/openproject/data/pgdata/:/var/openproject/pgdata
      - /volume1/storage/docker-data/openproject/data/assets/:/var/openproject/assets
    environment:
      DATABASE_URL: "postgresql://postgres:***REMOVED***@192.168.2.18:5432/openproject?sslmode=disable"
      OPENPROJECT_SECRET_KEY_BASE: secret
      OPENPROJECT_HOST__NAME: ""
      OPENPROJECT_HTTPS: false
    restart: always
```