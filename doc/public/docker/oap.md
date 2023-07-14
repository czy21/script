# dockerfile

# docker-compose
```shell
docker-compose --project-name oap --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:
  skywalking-oap:
    image: apache/skywalking-oap-server:9.0.0
    container_name: skywalking-oap
    privileged: true
    user: root
    environment:
      SW_HEALTH_CHECKER: default
      SW_OTEL_RECEIVER: default
      SW_OTEL_RECEIVER_ENABLED_OC_RULES: vm
      SW_STORAGE: elasticsearch
      SW_STORAGE_ES_CLUSTER_NODES: <domain>:80
      SW_ES_USER: <username>
      SW_ES_PASSWORD: <password>
      SW_TELEMETRY: prometheus
      SW_PROMETHEUS_FETCHER: default
      JAVA_OPTS: "-Xms2048m -Xmx2048m"

    healthcheck:
      test: [ "CMD-SHELL", "/skywalking/bin/swctl ch" ]
      interval: 30s
      timeout: 10s
      retries: 3

  skywalking-web:
    image: apache/skywalking-ui
    container_name: skywalking-ui
    privileged: true
    user: root
    ports:
      - "8090:8080"
    environment:
      SW_OAP_ADDRESS: http://skywalking-oap:12800


```