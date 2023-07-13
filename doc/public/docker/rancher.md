# dockerfile

# docker-compose
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
      - /volume1/storage/docker-data/rancher/cni/:/var/lib/cni/
      - /volume1/storage/docker-data/rancher/kubelet/:/var/lib/kubelet/
      - /volume1/storage/docker-data/rancher/data/:/var/lib/rancher
      - /volume1/storage/docker-data/rancher/log/:/var/log/
    command:
      - --no-cacerts
    restart: always
```