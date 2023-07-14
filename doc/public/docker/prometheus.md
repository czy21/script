
## docker-compose
```bash
docker-compose --project-name prometheus --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.prometheus.service: prometheus
  traefik.http.services.prometheus.loadbalancer.server.port: 9090

services:

  prometheus:
    image: prom/prometheus
    container_name: prometheus
    labels:
      <<: *traefik-label
    privileged: true
    volumes:
      - /volume5/storage/docker-data/prometheus/conf/:/etc/prometheus/
      - /volume5/storage/docker-data/prometheus/data/:/prometheus/
    command:
      - --config.file=/etc/prometheus/prometheus.yml
      - --storage.tsdb.path=/prometheus
      - --web.console.libraries=/usr/share/prometheus/console_libraries
      - --web.console.templates=/usr/share/prometheus/consoles
      - --storage.tsdb.no-lockfile
      - --storage.tsdb.retention.time=7d
      - --web.enable-lifecycle
    user: root
    restart: always

```