# dockerfile

# docker-compose
```shell
docker-compose --project-name jaeger --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-db-common: &db-common
  SPAN_STORAGE_TYPE: elasticsearch
  ES_SERVER_URLS: http://es.czy21-internal.com:80
  ES_USERNAME: "admin"
  ES_PASSWORD: "***REMOVED***"

x-traefik-collector-label: &traefik-collector-label
  traefik.enable: true
  traefik.http.routers.jaeger-collector.service: jaeger-collector
  traefik.http.services.jaeger-collector.loadbalancer.server.port: 14250

x-traefik-query-label: &traefik-query-label
  traefik.enable: true
  traefik.http.routers.jaeger-query.service: jaeger-query
  traefik.http.services.jaeger-query.loadbalancer.server.port: 16686

services:

  
  jaeger-collector-1:
    image: jaegertracing/jaeger-collector:1.42.0
    container_name: jaeger-collector-1
    hostname: jaeger-collector-1
    labels:
      <<: *traefik-collector-label
    expose:
      - "14250"
    environment:
      <<: *db-common
    restart: always
  
  jaeger-collector-2:
    image: jaegertracing/jaeger-collector:1.42.0
    container_name: jaeger-collector-2
    hostname: jaeger-collector-2
    labels:
      <<: *traefik-collector-label
    expose:
      - "14250"
    environment:
      <<: *db-common
    restart: always
  

  jaeger-agent:
    image: jaegertracing/jaeger-agent:1.42.0
    pull_policy: always
    container_name: jaeger-agent
    ports:
      - "5778:5778"
      - "6831:6831/udp"
    environment:
      REPORTER_GRPC_HOST_PORT: jaeger-collector.czy21-internal.com:80
    restart: always

  jaeger-query:
    image: jaegertracing/jaeger-query:1.42.0
    pull_policy: always
    container_name: jaeger-query
    labels:
      <<: *traefik-query-label
    expose:
      - "16686"
    environment:
      <<: *db-common
    restart: always
```