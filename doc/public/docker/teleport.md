## conf
- /volume5/storage/docker-data/teleport/conf/teleport.yaml
```text
teleport:
  data_dir: /var/lib/teleport
  log:
    output: stderr
    severity: INFO
auth_service:
  cluster_name: main
  enabled: "yes"
  authentication:
    type: local
    second_factor: off
  proxy_listener_mode: multiplex
ssh_service:
  enabled: "yes"
  labels:
    env: example
  commands:
  - name: hostname
    command: [hostname]
    period: 1m0s
proxy_service:
  enabled: "yes"
  web_listen_addr: "0.0.0.0:80"
```
## docker-compose
```bash
docker-compose --project-name teleport --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.teleport.service: teleport
  traefik.http.services.teleport.loadbalancer.server.port: 80

services:
  teleport:
    image: public.ecr.aws/gravitational/teleport-lab:10
    container_name: teleport
    hostname: teleport
    labels:
      <<: *traefik-label
    entrypoint: /bin/sh
    command: -c "/usr/bin/dumb-init teleport start -d -c /etc/teleport.d/teleport.yaml --insecure --insecure-no-tls"
    expose:
      - "80"
    volumes:
      - /volume5/storage/docker-data/teleport/data/empty/:/teleport/
      - /volume5/storage/docker-data/teleport/conf/teleport.yaml:/etc/teleport.d/teleport.yaml
      - /volume5/storage/docker-data/teleport/data/data/:/var/lib/teleport
```