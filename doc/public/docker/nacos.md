# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.nacos.service: nacos
  traefik.http.services.nacos.loadbalancer.server.port: 8848

services:

  nacos:
    image: nacos/nacos-server:v2.2.0
    pull_policy: always
    container_name: "nacos"
    hostname: "nacos"
    privileged: true
    user: root
    labels:
      <<: *traefik-label
    ports:
      - "8848:8848"
      - "9848:9848"
    environment:
      PREFER_HOST_MODE: hostname
      MODE: standalone
      SPRING_DATASOURCE_PLATFORM: mysql
      MYSQL_SERVICE_HOST: "<ip>"
      MYSQL_SERVICE_DB_NAME: nacos
      MYSQL_SERVICE_PORT: "3306"
      MYSQL_SERVICE_USER: "<username>"
      MYSQL_SERVICE_PASSWORD: "<password>"
      MYSQL_SERVICE_DB_PARAM: characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&serverTimezone=UTC
    restart: always
```