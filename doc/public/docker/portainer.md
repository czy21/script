
## conf
- /volume5/storage/docker-data/portainer/conf/portainer_password
```text
<password>
```
## docker-compose
```bash
docker-compose --project-name portainer --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.portainer.service: portainer
  traefik.http.services.portainer.loadbalancer.server.port: 9000

services:
  portainer:
    image: portainer/portainer-ce:2.18.4-alpine
    container_name: portainer
    labels:
      <<: *traefik-label
    privileged: true
    expose:
      - "9000"
      - "8000"
      - "9443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /volume5/storage/docker-data/portainer/data:/data/
      - /volume5/storage/docker-data/portainer/conf/portainer_password:/tmp/portainer_password
    command: --admin-password-file /tmp/portainer_password
#    networks:
#      macvlan100:
#        ipv4_address: 192.168.2.147
    restart: always
```