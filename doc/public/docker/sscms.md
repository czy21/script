
## docker-compose
```bash
docker-compose --project-name sscms --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.sscms.service: sscms
  traefik.http.services.sscms.loadbalancer.server.port: 80

services:
  sscms:
    image: sscms/core:7.2.1
    container_name: sscms
    hostname: sscms
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "80"
    volumes:
      - /volume5/storage/docker-data/sscms/data/:/app/wwwroot
    environment:
      SSCMS_DATABASE_TYPE: SQLite
      SSCMS_SECURITY_KEY: e2a3d303-ac9b-41ff-9154-930710af0845
#      SSCMS_DATABASE_TYPE: MySQL
#      SSCMS_DATABASE_HOST: "<ip>"
#      SSCMS_DATABASE_PORT: "3306"
#      SSCMS_DATABASE_USER: "<username>"
#      SSCMS_DATABASE_PASSWORD: "<password>"
#      SSCMS_DATABASE_NAME: sscms
    restart: always
```