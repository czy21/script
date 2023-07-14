
## docker-compose
```bash
docker-compose --project-name sqle --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.sqle.service: sqle
  traefik.http.services.sqle.loadbalancer.server.port: 10000

services:

  sqle:
    image: actiontech/sqle-ce
    container_name: sqle
    labels:
      <<: *traefik-label
    privileged: true
    expose:
      - "10000"
    user: root
    environment:
      MYSQL_HOST: '<ip>'
      MYSQL_PORT: '3306'
      MYSQL_USER: '<username>'
      MYSQL_PASSWORD: '<password>'
      MYSQL_SCHEMA: "sqle"
    restart: always
```