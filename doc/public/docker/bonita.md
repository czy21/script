# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.bonita.service: bonita
  traefik.http.services.bonita.loadbalancer.server.port: 8080

services:
  bonita:
    image: bonita:7.14.0
    container_name: bonita
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "8080"
    environment:
      DB_VENDOR: mysql
      DB_NAME: bonita
      DB_HOST: '<ip>'
      DB_PORT: '3306'
      DB_USER: '<username>'
      DB_PASS: '<password>'
      BIZ_DB_NAME: bonita_home
      BIZ_DB_USER: '<username>'
      BIZ_DB_PASS: '<password>'
      TENANT_LOGIN: '<username>'
      TENANT_PASSWORD: '<password>'
      PLATFORM_LOGIN: '<username>'
      PLATFORM_PASSWORD: '<password>'
    entrypoint:
      - bash
      - -c
      - |
        exec /opt/files/startup.sh /opt/bonita/server/bin/catalina.sh run
```