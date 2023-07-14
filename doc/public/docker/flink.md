# dockerfile

# docker-compose
```shell
docker-compose --project-name flink --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-flink-common: &flink-common
  image: registry.czy21-public.com/library/flink
  privileged: true
  user: root
  pull_policy: always

x-traefik-jmr-label: &traefik-jmr-label
  traefik.enable: true
  traefik.http.routers.flink-jmr.service: flink-jmr
  traefik.http.services.flink-jmr.loadbalancer.server.port: 8081

x-traefik-his-label: &traefik-his-label
  traefik.enable: true
  traefik.http.routers.flink-his.service: flink-his
  traefik.http.services.flink-his.loadbalancer.server.port: 8081

services:
  flink-jmr:
    <<: *flink-common
    container_name: flink-jmr
    hostname: flink-jmr
    labels:
      <<: *traefik-jmr-label
    volumes:
      - /volume5/storage/docker-data/flink/data/:/data/
      - /volume5/storage/docker-data/flink/log/:/opt/flink/log/
    environment:
      FLINK_PROPERTIES: |
        jobmanager.rpc.address: flink-jmr
        parallelism.default: 2
        jobmanager.archive.fs.dir: file:///data/completed-jobs
        web.upload.dir: /data/jar
    command: jobmanager
    restart: always

  
  flink-tmr-1:
    <<: *flink-common
    container_name: flink-tmr-1
    hostname: flink-tmr1
    volumes:
      - /volume5/storage/docker-data/flink/log/:/opt/flink/log/
    environment:
      FLINK_PROPERTIES: |
        jobmanager.rpc.address: flink-jmr
        parallelism.default: 2
    command: taskmanager
    restart: always
  
  flink-tmr-2:
    <<: *flink-common
    container_name: flink-tmr-2
    hostname: flink-tmr2
    volumes:
      - /volume5/storage/docker-data/flink/log/:/opt/flink/log/
    environment:
      FLINK_PROPERTIES: |
        jobmanager.rpc.address: flink-jmr
        parallelism.default: 2
    command: taskmanager
    restart: always
  

  flink-his:
    <<: *flink-common
    container_name: flink-his
    hostname: flink-his
    labels:
      <<: *traefik-his-label
    volumes:
      - /volume5/storage/docker-data/flink/data/:/data/
      - /volume5/storage/docker-data/flink/log/:/opt/flink/log/
    environment:
      FLINK_PROPERTIES: |
        historyserver.web.address: flink-his
        historyserver.web.port: 8081
        historyserver.archive.fs.dir: file:///data/completed-jobs
        historyserver.archive.fs.refresh-interval: 10000
    command: history-server
    restart: always



```