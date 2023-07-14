
## docker-compose
```bash
docker-compose --project-name youtrack --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.youtrack.service: youtrack
  traefik.http.services.youtrack.loadbalancer.server.port: 8080

services:

  youtrack:
    image: jetbrains/youtrack:2022.3.63553
    container_name: youtrack
    hostname: youtrack
    expose:
      - "8080"
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    volumes:
      - /volume5/storage/docker-data/youtrack/data/data/:/opt/youtrack/data/
      - /volume5/storage/docker-data/youtrack/data/conf/:/opt/youtrack/conf/
      - /volume5/storage/docker-data/youtrack/data/logs/:/opt/youtrack/logs/
      - /volume5/storage/docker-data/youtrack/data/backups/:/opt/youtrack/backups/
    restart: always
```