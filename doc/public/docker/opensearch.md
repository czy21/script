
## conf
- /volume5/storage/docker-data/opensearch-1/conf/setup.sh
```bash
#!/bin/bash

for ((i=1;i<=2;i++));do
 data_node_dir=/usr/share/opensearch/data/${i}
 mkdir -p ${data_node_dir} && chown -R 1000:0 ${data_node_dir}
done

echo "Waiting for Opensearch availability";
until curl -s http://opensearch-1-1:9200 | grep -q "opensearch-1-1"; do sleep 30; done;

echo "All done!";
```
## docker-compose
```bash
docker-compose --project-name opensearch-1 --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-app-common: &app-common
  image: opensearchproject/opensearch:2.9.0

x-traefik-opensearch-label: &traefik-opensearch-label
  traefik.enable: true
  traefik.http.routers.opensearch-1.service: opensearch-1
  traefik.http.services.opensearch-1.loadbalancer.server.port: 9200

x-traefik-opensearch-dashboard-label: &traefik-opensearch-dashboard-label
  traefik.enable: true
  traefik.http.routers.opensearch-1-dashboard.service: opensearch-1-dashboard
  traefik.http.services.opensearch-1-dashboard.loadbalancer.server.port: 5601

services:
  opensearch-1-setup:
    <<: *app-common
    container_name: opensearch-1-setup
    command: sh ./setup.sh
    user: "0"
    working_dir: /usr/share/opensearch
    volumes:
      - /volume5/storage/docker-data/opensearch-1/conf/setup.sh:/usr/share/opensearch/setup.sh
      - /volume5/storage/docker-data/opensearch-1/data/:/usr/share/opensearch/data/
    healthcheck:
      test: ["CMD-SHELL", "[ -d /usr/share/opensearch/data/1 ]"]
      interval: 1s
      timeout: 5s
      retries: 120
  
  opensearch-1-1:
    <<: *app-common
    container_name: opensearch-1-1
    hostname: opensearch-1-1
    labels:
      <<: *traefik-opensearch-label
    expose:
      - "9200"
      - "9600"
    environment:
      OPENSEARCH_JAVA_OPTS: "-Xms512m -Xmx512m"
      node.name: opensearch-1-1
      cluster.name: opensearch-1
      cluster.initial_cluster_manager_nodes: opensearch-1-1,opensearch-1-2
      discovery.seed_hosts: opensearch-1-1,opensearch-1-2
      bootstrap.memory_lock: "true"
      DISABLE_SECURITY_PLUGIN: "true"
    volumes:
      - /volume5/storage/docker-data/opensearch-1/data/1/:/usr/share/opensearch/data/
    deploy:
      resources:
        limits:
          memory: 8g
    ulimits:
      memlock:
        soft: -1 # Set memlock to unlimited (no soft or hard limit)
        hard: -1
      nofile:
        soft: 65536 # Maximum number of open files for the opensearch user - set to at least 65536
        hard: 65536
    depends_on:
      opensearch-1-setup:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL","curl -s http://localhost:9200 | grep -q 'opensearch-1-1'"]
      interval: 10s
      timeout: 10s
      retries: 120
  opensearch-1-2:
    <<: *app-common
    container_name: opensearch-1-2
    hostname: opensearch-1-2
    labels:
      <<: *traefik-opensearch-label
    expose:
      - "9200"
      - "9600"
    environment:
      OPENSEARCH_JAVA_OPTS: "-Xms512m -Xmx512m"
      node.name: opensearch-1-2
      cluster.name: opensearch-1
      cluster.initial_cluster_manager_nodes: opensearch-1-1,opensearch-1-2
      discovery.seed_hosts: opensearch-1-1,opensearch-1-2
      bootstrap.memory_lock: "true"
      DISABLE_SECURITY_PLUGIN: "true"
    volumes:
      - /volume5/storage/docker-data/opensearch-1/data/2/:/usr/share/opensearch/data/
    deploy:
      resources:
        limits:
          memory: 8g
    ulimits:
      memlock:
        soft: -1 # Set memlock to unlimited (no soft or hard limit)
        hard: -1
      nofile:
        soft: 65536 # Maximum number of open files for the opensearch user - set to at least 65536
        hard: 65536
    depends_on:
      - opensearch-1-1
    healthcheck:
      test: ["CMD-SHELL","curl -s http://localhost:9200 | grep -q 'opensearch-1-2'"]
      interval: 10s
      timeout: 10s
      retries: 120
  opensearch-1-dashboard:
    image: opensearchproject/opensearch-dashboards:2.9.0
    container_name: opensearch-1-dashboard
    labels:
      <<: *traefik-opensearch-dashboard-label
    expose:
      - "5601"
    environment:
      OPENSEARCH_HOSTS: '["http://opensearch-1-1:9200", "http://opensearch-1-2:9200"]'
      DISABLE_SECURITY_DASHBOARDS_PLUGIN: "true"
```