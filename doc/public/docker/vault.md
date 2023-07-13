# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.vault.service: vault
  traefik.http.services.vault.loadbalancer.server.port: 8200

services:
  vault:
    image: vault:1.11.3
    container_name: vault
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    cap_add:
       - IPC_LOCK
    expose:
      - "8200"
    volumes:
      - /volume1/storage/docker-data/vault/data/file/:/vault/file/
      - /volume1/storage/docker-data/vault/data/logs/:/vault/logs/
    environment:
      VAULT_LOCAL_CONFIG: '{"backend": {"file": {"path": "/vault/file"}}, "default_lease_ttl": "168h", "max_lease_ttl": "720h"}'
```