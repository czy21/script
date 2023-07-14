
## docker-compose
```bash
docker-compose --project-name crate-1 --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-app-common: &app-common
  image: crate:5.0.1

x-traefik-web-label: &traefik-web-label
  traefik.enable: true
  traefik.http.routers.crate-1.service: crate-1
  traefik.http.services.crate-1.loadbalancer.server.port: 4200

services:
  
  crate-1-1:
    <<: *app-common
    container_name: crate-1-1
    hostname: crate-1-1
    labels:
      <<: *traefik-web-label
    expose:
      - "4200"
    ports:
      - '4201:4200'
      - '5401:5432'
    volumes:
      - /volume5/storage/docker-data/crate-1/data/1/:/data/
    command:
      - "crate"
      - "-Ccluster.name=crate-1"
      - "-Cnode.name=crate-1-1"
      - "-Cnode.data=true"
      - "-Cnetwork.host=_site_"
      - "-Cdiscovery.seed_hosts=crate-1-2,crate-1-3"
      - "-Ccluster.initial_master_nodes=crate-1-1,crate-1-2,crate-1-3"
      - "-Cgateway.expected_data_nodes=3"
      - "-Cgateway.recover_after_data_nodes=2"
    environment:
      CRATE_HEAP_SIZE: 2g
  crate-1-2:
    <<: *app-common
    container_name: crate-1-2
    hostname: crate-1-2
    labels:
      <<: *traefik-web-label
    expose:
      - "4200"
    ports:
      - '4202:4200'
      - '5402:5432'
    volumes:
      - /volume5/storage/docker-data/crate-1/data/2/:/data/
    command:
      - "crate"
      - "-Ccluster.name=crate-1"
      - "-Cnode.name=crate-1-2"
      - "-Cnode.data=true"
      - "-Cnetwork.host=_site_"
      - "-Cdiscovery.seed_hosts=crate-1-1,crate-1-3"
      - "-Ccluster.initial_master_nodes=crate-1-1,crate-1-2,crate-1-3"
      - "-Cgateway.expected_data_nodes=3"
      - "-Cgateway.recover_after_data_nodes=2"
    environment:
      CRATE_HEAP_SIZE: 2g
  crate-1-3:
    <<: *app-common
    container_name: crate-1-3
    hostname: crate-1-3
    labels:
      <<: *traefik-web-label
    expose:
      - "4200"
    ports:
      - '4203:4200'
      - '5403:5432'
    volumes:
      - /volume5/storage/docker-data/crate-1/data/3/:/data/
    command:
      - "crate"
      - "-Ccluster.name=crate-1"
      - "-Cnode.name=crate-1-3"
      - "-Cnode.data=true"
      - "-Cnetwork.host=_site_"
      - "-Cdiscovery.seed_hosts=crate-1-1,crate-1-2"
      - "-Ccluster.initial_master_nodes=crate-1-1,crate-1-2,crate-1-3"
      - "-Cgateway.expected_data_nodes=3"
      - "-Cgateway.recover_after_data_nodes=2"
    environment:
      CRATE_HEAP_SIZE: 2g
```