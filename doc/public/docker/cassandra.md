
## docker-compose
```bash
docker-compose --project-name cassandra-1 --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-app-common: &app-common
  image: cassandra:4.1.0

x-traefik-cassandra-label: &traefik-cassandra-label
  traefik.enable: true
  traefik.http.routers.cassandra-1.service: cassandra-1
  traefik.http.services.cassandra-1.loadbalancer.server.port: 7000

services:
  cassandra-1-1:
    <<: *app-common
    container_name: cassandra-1-1
    hostname: cassandra-1-1
    labels:
      <<: *traefik-cassandra-label
    volumes:
      - /volume5/storage/docker-data/cassandra-1/data/1/:/var/lib/cassandra/
  cassandra-1-2:
    <<: *app-common
    container_name: cassandra-1-2
    hostname: cassandra-1-2
    labels:
      <<: *traefik-cassandra-label
    volumes:
      - /volume5/storage/docker-data/cassandra-1/data/2/:/var/lib/cassandra/
    environment:
      CASSANDRA_SEEDS: cassandra-1-1
```