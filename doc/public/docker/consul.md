# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.consul.service: consul
  traefik.http.services.consul.loadbalancer.server.port: 8500

services:

  consul:
    image: consul:1.15.0
    container_name: consul
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    volumes:
      - /volume1/storage/docker-data/consul/data/:/consul/data/
      - /volume1/storage/docker-data/consul/conf/:/consul/config/
    command: 'agent -server -ui -node=server-1 -bootstrap-expect=1 -client=0.0.0.0 -datacenter=nas'
    restart: always
```