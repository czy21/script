
## conf
- /volume5/storage/docker-data/gocd/conf/db.properties
```text
db.driver=com.mysql.cj.jdbc.Driver
db.url=jdbc:mysql://<ip>:/gocd
db.user=<username>
db.password=<password>
```
## docker-compose
```bash
docker-compose --project-name gocd --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.gocd.service: gocd
  traefik.http.services.gocd.loadbalancer.server.port: 8153

services:

  gocd:
    image: gocd/gocd-server:v23.3.0
    container_name: gocd
    hostname: gocd
    privileged: true
    user: root
    labels:
      <<: *traefik-label
    expose:
      - "8153"
    volumes:
      - /volume5/storage/docker-data/gocd/data/:/home/go/
      - /volume5/storage/docker-data/gocd/conf/db.properties:/godata/config/db.properties
    restart: always
```