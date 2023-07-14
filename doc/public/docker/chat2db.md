
## docker-compose
```bash
docker-compose --project-name chat2db --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.chat2db.service: chat2db
  traefik.http.services.chat2db.loadbalancer.server.port: 10824

services:
  chat2db:
    image: "registry.czy21-public.com/library/chat2db"
    container_name: chat2db
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "10824"
    volumes:
      - /volume5/storage/docker-data/chat2db/data/:/data/
    environment:
      JAVA_OPTS: "-Dspring.datasource.url=jdbc:h2:/data/db/chat2db;MODE=MYSQL"
      LOG_PATH: "/data/log/"
    restart: always
```