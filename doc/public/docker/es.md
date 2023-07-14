
## conf
- /volume5/storage/docker-data/es-1/conf/instance.yml
```text
instances:
  - name: es-1-1
    dns:
      - es-1-1
      - localhost
    ip:
      - 127.0.0.1
  
  - name: es-1-2
    dns:
      - es-1-2
      - localhost
    ip:
      - 127.0.0.1
  
```
- /volume5/storage/docker-data/es-1/conf/kibana.yml
```text
server:
  host: "0.0.0.0"

monitoring:
  ui:
    container:
      elasticsearch:
        enabled: true

elasticsearch:
  hosts: 
    - http://es-1-1:9200
  username: <username>
  password: <password>
```
- /volume5/storage/docker-data/es-1/conf/setup.sh
```text
#!/bin/bash

for ((i=1;i<=2;i++));do
 data_node_dir=/usr/share/elasticsearch/data/${i}
 mkdir -p ${data_node_dir} && chown -R 1000:0 ${data_node_dir}
done

cert_path=/usr/share/elasticsearch/config/cert

echo "Creating CA";
bin/elasticsearch-certutil ca --silent --pem -out ${cert_path}/ca.zip;
unzip -n ${cert_path}/ca.zip -d ${cert_path};

echo "Creating cert";
bin/elasticsearch-certutil cert --ca-cert ${cert_path}/ca/ca.crt --ca-key ${cert_path}/ca/ca.key --silent --pem --in config/instance.yml -out ${cert_path}/cert.zip;
unzip -n ${cert_path}/cert.zip -d ${cert_path}/

rm -rf ${cert_path}/ca.zip ${cert_path}/cert.zip
chown -R root:root ${cert_path}

echo "Waiting for Elasticsearch availability";
until curl -s http://es-1-1:9200 | grep -q "missing authentication credentials"; do sleep 30; done;

echo "All done!";
```
- /volume5/storage/docker-data/es-1/conf/users
```text
<username>:$2b$12$9ux91iTlGkiNaZQ1NEYk0.K2zKFcn3WTAbSfWkm..3QoybGd/oQ6W
```
- /volume5/storage/docker-data/es-1/conf/users_roles
```text
superuser:<username>
kibana_system:<username>
```
## docker-compose
```bash
docker-compose --project-name es-1 --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-app-common: &app-common
  image: elasticsearch:7.17.10

x-traefik-es-label: &traefik-es-label
  traefik.enable: true
  traefik.http.routers.es-1.service: es-1
  traefik.http.services.es-1.loadbalancer.server.port: 9200

x-traefik-kb-label: &traefik-kb-label
  traefik.enable: true
  traefik.http.routers.es-1-kb.service: es-1-kb
  traefik.http.services.es-1-kb.loadbalancer.server.port: 5601

services:
  es-1-setup:
    <<: *app-common
    container_name: es-1-setup
    command: sh ./setup.sh
    user: "0"
    working_dir: /usr/share/elasticsearch
    volumes:
      - /volume5/storage/docker-data/es-1/conf/setup.sh:/usr/share/elasticsearch/setup.sh
      - /volume5/storage/docker-data/es-1/conf/instance.yml/:/usr/share/elasticsearch/config/instance.yml
      - /volume5/storage/docker-data/es-1/cert/:/usr/share/elasticsearch/config/cert/
      - /volume5/storage/docker-data/es-1/data/:/usr/share/elasticsearch/data/
    healthcheck:
      test: ["CMD-SHELL", "[ -f /usr/share/elasticsearch/config/cert/es-1-1/es-1-1.crt ]"]
      interval: 1s
      timeout: 5s
      retries: 120
  
  es-1-1:
    <<: *app-common
    container_name: es-1-1
    hostname: es-1-1
    labels:
      <<: *traefik-es-label
    expose:
      - "9200"
    environment:
      # ES_JAVA_OPTS: -Xms4g -Xmx4g
      node.name: es-1-1
      cluster.name: es-1
      cluster.initial_master_nodes: es-1-1,es-1-2
      discovery.seed_hosts: es-1-2
      bootstrap.memory_lock: "true"
      ELASTIC_PASSWORD: <password>
      xpack.security.enabled: true
      xpack.security.http.ssl.enabled: false
      xpack.security.transport.ssl.enabled: true
      xpack.security.transport.ssl.verification_mode: certificate
      xpack.security.transport.ssl.certificate_authorities: /usr/share/elasticsearch/config/cert/ca/ca.crt
      xpack.security.transport.ssl.certificate: /usr/share/elasticsearch/config/cert/es-1-1/es-1-1.crt
      xpack.security.transport.ssl.key: /usr/share/elasticsearch/config/cert/es-1-1/es-1-1.key
      xpack.security.authc.realms.file.file1.order: 0
      xpack.security.authc.realms.native.realm1.order: 1
      xpack.monitoring.collection.enabled: true
    volumes:
      - /volume5/storage/docker-data/es-1/conf/users:/usr/share/elasticsearch/config/users
      - /volume5/storage/docker-data/es-1/conf/users_roles:/usr/share/elasticsearch/config/users_roles
      - /volume5/storage/docker-data/es-1/data/1/:/usr/share/elasticsearch/data/
      - /volume5/storage/docker-data/es-1/cert/:/usr/share/elasticsearch/config/cert/
    deploy:
      resources:
        limits:
          memory: 8g
    ulimits:
      memlock:
        soft: -1
        hard: -1
    depends_on:
      es-1-setup:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL","curl -s http://localhost:9200 | grep -q 'missing authentication credentials'"]
      interval: 10s
      timeout: 10s
      retries: 120
  es-1-2:
    <<: *app-common
    container_name: es-1-2
    hostname: es-1-2
    labels:
      <<: *traefik-es-label
    expose:
      - "9200"
    environment:
      # ES_JAVA_OPTS: -Xms4g -Xmx4g
      node.name: es-1-2
      cluster.name: es-1
      cluster.initial_master_nodes: es-1-1,es-1-2
      discovery.seed_hosts: es-1-1
      bootstrap.memory_lock: "true"
      ELASTIC_PASSWORD: <password>
      xpack.security.enabled: true
      xpack.security.http.ssl.enabled: false
      xpack.security.transport.ssl.enabled: true
      xpack.security.transport.ssl.verification_mode: certificate
      xpack.security.transport.ssl.certificate_authorities: /usr/share/elasticsearch/config/cert/ca/ca.crt
      xpack.security.transport.ssl.certificate: /usr/share/elasticsearch/config/cert/es-1-2/es-1-2.crt
      xpack.security.transport.ssl.key: /usr/share/elasticsearch/config/cert/es-1-2/es-1-2.key
      xpack.security.authc.realms.file.file1.order: 0
      xpack.security.authc.realms.native.realm1.order: 1
      xpack.monitoring.collection.enabled: true
    volumes:
      - /volume5/storage/docker-data/es-1/conf/users:/usr/share/elasticsearch/config/users
      - /volume5/storage/docker-data/es-1/conf/users_roles:/usr/share/elasticsearch/config/users_roles
      - /volume5/storage/docker-data/es-1/data/2/:/usr/share/elasticsearch/data/
      - /volume5/storage/docker-data/es-1/cert/:/usr/share/elasticsearch/config/cert/
    deploy:
      resources:
        limits:
          memory: 8g
    ulimits:
      memlock:
        soft: -1
        hard: -1
    depends_on:
      - es-1-1
    healthcheck:
      test: ["CMD-SHELL","curl -s http://localhost:9200 | grep -q 'missing authentication credentials'"]
      interval: 10s
      timeout: 10s
      retries: 120
  es-1-kb:
    image: kibana:7.17.10
    container_name: es-1-kb
    labels:
      <<: *traefik-kb-label
    expose:
      - "5601"
    volumes:
      - /volume5/storage/docker-data/es-1/conf/kibana.yml:/usr/share/kibana/config/kibana.yml
    depends_on:
      es-1-1:
        condition: service_healthy
      es-1-2:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL","curl -s -I http://localhost:5601 | grep -q 'HTTP/1.1 302 Found'"]
      interval: 10s
      timeout: 10s
      retries: 120
```