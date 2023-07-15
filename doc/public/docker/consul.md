
## conf
- /volume5/storage/docker-data/consul/conf/acl.json
```text
{
  "acl": {
    "enabled": true,
    "default_policy": "deny",
    "enable_token_persistence": true,
    "tokens": {
      "initial_management": "b0bc3475-ea2c-c1ed-4c0b-f8de1dc04784"
    }
  }
}
```
## docker-compose
```bash
docker-compose --project-name consul --file docker-compose.yaml up --detach --build --remove-orphans
```
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
      - /volume5/storage/docker-data/consul/data/:/consul/data/
      - /volume5/storage/docker-data/consul/conf/:/consul/config/
    command: 'agent -server -ui -node=server-1 -bootstrap-expect=1 -client=0.0.0.0 -datacenter=nas'
    restart: always
```