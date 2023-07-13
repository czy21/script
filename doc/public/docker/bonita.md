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
      DB_HOST: '192.168.2.18'
      DB_PORT: '3306'
      DB_USER: 'admin'
      DB_PASS: 'Czy.190815'
      BIZ_DB_NAME: bonita_home
      BIZ_DB_USER: 'admin'
      BIZ_DB_PASS: 'Czy.190815'
      TENANT_LOGIN: 'admin'
      TENANT_PASSWORD: 'Czy20210314.'
      PLATFORM_LOGIN: 'admin'
      PLATFORM_PASSWORD: 'Czy20210314.'
    entrypoint:
      - bash
      - -c
      - |
        exec /opt/files/startup.sh /opt/bonita/server/bin/catalina.sh run
```