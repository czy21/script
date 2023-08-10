
## conf
- /volume5/storage/docker-data/traefik/conf/traefik.yml
```yaml
providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
    defaultRule: ""
  file:
    directory: /etc/traefik/conf.d/
    watch: true

log:
  level: ERROR # DEBUG, PANIC, FATAL, ERROR, WARN, INFO
  filePath: /dev/stdout

accessLog:
  filePath: /dev/stdout

api:
  insecure: true

entryPoints:
  web:
    address: :80
  websecure:
    address: :443
  traefik:
    address: :8080
  metrics:
    address: :8082

metrics:
  prometheus:
    entryPoint: metrics
```
- /volume5/storage/docker-data/traefik/conf/conf.d/base.yml
```yaml
http:
  routers:
    metrics:
      rule: Host(`traefik-.czy21-internal.com`) && PathPrefix(`/metrics`)
      service: prometheus@internal
    traefik:
      rule: Host(`traefik-.czy21-internal.com`)
      service: traefik@docker
    cadvisor:
      rule: Host(`cadvisor-.czy21-internal.com`)
      service: cadvisor@docker
    nginx-exporter:
      rule: Host(`nginx-exporter-.czy21-internal.com`)
      service: nginx-exporter@docker
    fluent-bit-log-metrics:
      rule: Host(`fluent-bit--log-metrics.czy21-internal.com`)
      service: fluent-bit-log-metrics@docker
```
## docker-compose
```bash
docker-compose --project-name traefik --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.traefik.service: traefik
  traefik.http.services.traefik.loadbalancer.server.port: 8080

services:

  traefik:
    image: traefik:v2.10.4
    container_name: traefik
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "80"
      - "443"
      - "8080"
      - "8082"
    volumes:
      - /volume5/storage/docker-data/traefik/conf/traefik.yml:/etc/traefik/traefik.yml
      - /volume5/storage/docker-data/traefik/conf/conf.d/:/etc/traefik/conf.d/
      - /volume5/storage/docker-data/traefik/conf/cert/:/etc/traefik/cert/
      - /var/run/docker.sock:/var/run/docker.sock:ro
    restart: always
```