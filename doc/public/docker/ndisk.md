# dockerfile
# conf
- /volume5/storage/docker-data/ndisk/conf/app.yaml
```text
server:
  port: 8080

data:
  dav: data/dav

db:
  driver-name: mysql
  url: <username>:<password>@tcp(<ip>:3306)/ndisk?charset=utf8mb4&parseTime=True&loc=UTC

log:
#  file: app.log # if removed,log in console
  level: info # info,debug,error

cache:
  type: redis # redis,memory
  redis:
    url: redis://:<password>@<ip>:6379
  expire: 180 # seconds

dav:
  username: admin
  password: admin

cloud189:
  cookie: ''
```

# docker-compose
```shell
docker-compose --project-name ndisk --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.ndisk.service: ndisk
  traefik.http.services.ndisk.loadbalancer.server.port: 8080

services:

  ndisk:
    image: registry.czy21-public.com/library/ndisk:latest
    pull_policy: always
    container_name: ndisk
    labels:
      <<: *traefik-label
    expose:
      - "8080"
    volumes:
      - /volume5/storage/docker-data/ndisk/conf/app.yaml:/app/app.yaml
      - /volume5/storage/docker-data/ndisk/data/:/data/
    environment:
      CONFIG_FILE: /app/app.yaml
    restart: always
```