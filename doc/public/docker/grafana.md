# dockerfile

# docker-compose
```shell
docker-compose --project-name grafana --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.grafana.service: grafana
  traefik.http.services.grafana.loadbalancer.server.port: 3000

services:
  grafana:
    image: grafana/grafana:9.2.2
    container_name: grafana
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    volumes:
      - /volume1/storage/docker-data/grafana/conf/grafana.ini:/etc/grafana/grafana.ini
      - /volume1/storage/docker-data/grafana/conf/datasources/:/etc/grafana/provisioning/datasources/
      - /volume1/storage/docker-data/grafana/conf/dashboards/:/etc/grafana/provisioning/dashboards/
      - /volume1/storage/docker-data/grafana/data/:/var/lib/grafana/
    environment:
      GF_INSTALL_PLUGINS: grafana-piechart-panel
    restart: always


```