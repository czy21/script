
## conf
- /volume5/storage/docker-data/go-pulsar-manager/conf/app.yaml
```text
web:
  port: 3000
  dist: /app/dist
server:
  port: 8080

db:
  driver-name: mysql
  url: admin:***REMOVED***@tcp(192.168.2.18:3306)/go-pulsar-manager?charset=utf8mb4&parseTime=True

log:
#  file: /app/log/app.log # if removed,log in console
  level: info # info,debug,error
```
## docker-compose
```bash
docker-compose --project-name go-pulsar-manager --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.go-pulsar-manager.service: go-pulsar-manager
  traefik.http.services.go-pulsar-manager.loadbalancer.server.port: 3000

services:

  go-pulsar-manager:
    image: registry.czy21-public.com/library/go-pulsar-manager:master
    container_name: go-pulsar-manager
    labels:
      <<: *traefik-label
    privileged: true
    expose:
      - "3000"
      - "8080"
    user: root
    volumes:
      - /volume5/storage/docker-data/go-pulsar-manager/conf/app.yaml:/app/app.yaml
      - /volume5/storage/docker-data/go-pulsar-manager/log/:/app/log/
    environment:
      TZ: Asia/Shanghai
      GIN_MODE: release
      GPM_CONFIG_FILE: /app/app.yaml


```