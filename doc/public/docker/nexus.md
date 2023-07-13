# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.nexus.service: nexus
  traefik.http.services.nexus.loadbalancer.server.port: 8081

services:
  nexus:
    image: sonatype/nexus3:3.57.0
    container_name: nexus
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "8081"
    volumes:
      - /volume1/storage/docker-data/nexus/data/:/nexus-data/
    environment:
      INSTALL4J_ADD_VM_PARAMS: -Xms4G -Xmx4G -XX:MaxDirectMemorySize=6717M
      NEXUS_SECURITY_INITIAL_PASSWORD: "<password>"
    restart: always
```