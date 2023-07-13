# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.pulsar-manager.service: pulsar-manager
  traefik.http.services.pulsar-manager.loadbalancer.server.port: 9527

services:

  pulsar-manager:
    image: registry.czy21-internal.com/library/pulsar-manager
    container_name: pulsar-manager
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "9527"
    volumes:
      - /volume1/storage/docker-data/pulsar-manager/log/web/:/var/log/nginx/
      - /volume1/storage/docker-data/pulsar-manager/log/api/:/log/
    environment:
      SPRING_CONFIGURATION_FILE: /opt/pulsar-manager/application.properties
      JAVA_ARGS: "
      --spring.datasource.driver-class-name=org.postgresql.Driver
      --spring.datasource.url=jdbc:postgresql://192.168.2.18:5432/pulsar_manager?user=postgres&password=***REMOVED***
      --spring.datasource.initialization-mode=NEVER
      "



```