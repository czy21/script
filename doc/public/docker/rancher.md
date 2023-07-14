# dockerfile

# docker-compose
```shell
docker-compose --project-name rancher --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.rancher.service: rancher
  traefik.http.services.rancher.loadbalancer.server.port: 80

services:

  rancher:
    image: rancher/rancher:v2.7-head
    container_name: rancher
    labels:
      <<: *traefik-label
    privileged: true
    ports:
      - "7443:443"
      - "7080:80"
    expose:
      - "80"
      - "443"
    volumes:
      - /volume5/storage/docker-data/rancher/cni/:/var/lib/cni/
      - /volume5/storage/docker-data/rancher/kubelet/:/var/lib/kubelet/
      - /volume5/storage/docker-data/rancher/data/:/var/lib/rancher
      - /volume5/storage/docker-data/rancher/log/:/var/log/
    command:
      - --no-cacerts
    restart: always
```