
## docker-compose
```bash
docker-compose --project-name halo --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.halo.service: halo
  traefik.http.services.halo.loadbalancer.server.port: 8090

services:
  halo:
    image: halohub/halo:2.8
    container_name: halo
    hostname: halo
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "8090"
    volumes:
      - /volume5/storage/docker-data/halo/data/:/root/.halo2/
    command:
      - --spring.sql.init.platform=mysql
      - --spring.r2dbc.url=r2dbc:pool:mysql://<ip>:3306/halo
      - --spring.r2dbc.username=<username>
      - --spring.r2dbc.password=<password>
      - --halo.security.initializer.superadminusername=<username>
      - --halo.security.initializer.superadminpassword=<password>
    restart: always
```