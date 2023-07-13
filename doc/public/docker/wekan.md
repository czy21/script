# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.wekan.service: wekan
  traefik.http.services.wekan.loadbalancer.server.port: 8080

services:

  wekan:
    image: wekanteam/wekan:v6.58
    container_name: wekan
    hostname: wekan
    expose:
      - "8080"
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    volumes:
      - /volume1/storage/docker-data/wekan/data/:/data/
    environment:
      MONGO_URL: mongodb://<username>:<password>@<ip>:27017/wekan?authSource=<username>
      WRITABLE_PATH: /data
      ROOT_URL: http://
    restart: always
```