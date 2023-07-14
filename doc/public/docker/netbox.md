# dockerfile

# docker-compose
```shell
docker-compose --project-name netbox --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.netbox.service: netbox
  traefik.http.services.netbox.loadbalancer.server.port: 8000

services:

  netbox:
    image: linuxserver/netbox:3.2.6
    container_name: netbox
    labels:
      <<: *traefik-label
    expose:
      - "8000"
    volumes:
      - /volume5/storage/docker-data/netbox/conf/:/config
    environment:
      PUID: 1000
      PGID: 1000
      TZ: Asia/Shanghai
      SUPERUSER_EMAIL: 805899926@qq.com
      SUPERUSER_PASSWORD: '<password>'
      ALLOWED_HOST: '*'
      DB_NAME: netbox
      DB_USER: 'postgres'
      DB_PASSWORD: '<password>'
      DB_HOST: '<ip>'
      DB_PORT: '5432'
      REDIS_HOST: '<ip>'
      REDIS_PORT: '6379'
      REDIS_PASSWORD: '<password>'
      REDIS_DB_TASK: 0
      REDIS_DB_CACHE: 0
    restart: always
```