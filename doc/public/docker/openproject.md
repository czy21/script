# dockerfile

# docker-compose
```shell
docker-compose --project-name openproject --file docker-compose.yaml up --detach --build --remove-orphans
```
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
      - /volume5/storage/docker-data/openproject/data/pgdata/:/var/openproject/pgdata
      - /volume5/storage/docker-data/openproject/data/assets/:/var/openproject/assets
    environment:
      DATABASE_URL: "postgresql://postgres:<password>@<ip>:5432/openproject?sslmode=disable"
      OPENPROJECT_SECRET_KEY_BASE: secret
      OPENPROJECT_HOST__NAME: ""
      OPENPROJECT_HTTPS: false
    restart: always
```