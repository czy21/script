# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.cadvisor.service: cadvisor
  traefik.http.services.cadvisor.loadbalancer.server.port: 8080

services:

  cadvisor:
    image: 'registry-proxy.czy21-internal.com/cadvisor/cadvisor:v0.47.1' # gcr.io/cadvisor/cadvisor:v0.47.1
    container_name: cadvisor
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    devices:
      - dev/kmsg
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /volume1/docker-root:/var/lib/docker:ro
    restart: always
```