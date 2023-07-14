
## docker-compose
```bash
docker-compose --project-name freeipa --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.freeipa.service: freeipa
  traefik.http.services.freeipa.loadbalancer.server.port: 80

services:

  freeipa:
    image: freeipa/freeipa-server:centos-9-stream-4.10.1
    pull_policy: always
    container_name: freeipa
    hostname: freeipa.czy21-internal.com
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    ports:
      - "389:389"
    volumes:
      - /volume5/storage/docker-data/freeipa/data/:/data/
      - /volume5/storage/docker-data/freeipa/run/:/run/
      - /volume5/storage/docker-data/freeipa/tmp/:/tmp/
      - /volume5/storage/docker-data/freeipa/log/://var/log/journal/
    command: ipa-server-install -U -r czy21-internal.com --no-ntp
    sysctls:
      - net.ipv6.conf.all.disable_ipv6=0
    environment:
      PASSWORD: "<password>"
    restart: always
```