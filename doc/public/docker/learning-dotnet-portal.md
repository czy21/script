# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.learning-dotnet-portal.service: learning-dotnet-portal
  traefik.http.services.learning-dotnet-portal.loadbalancer.server.port: 8080

services:
  learning-dotnet-portal:
    image: registry.czy21-internal.com/library/learning-dotnet-portal:master
    container_name: learning-dotnet-portal
    pull_policy: always
    labels:
      <<: *traefik-label
    volumes:
      - /volume1/storage/docker-data/learning-dotnet-portal/conf/appsettings.json:/app/appsettings.json
      - /volume1/storage/docker-data/learning-dotnet-portal/data/:/data/
    restart: always
```