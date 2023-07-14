# dockerfile
# conf
- /volume5/storage/docker-data/logstash/conf/logstash.yml
```text
http.host: "0.0.0.0"
xpack.monitoring.enabled: true
xpack.monitoring.elasticsearch.username: admin
xpack.monitoring.elasticsearch.password: ***REMOVED***
xpack.monitoring.elasticsearch.hosts: [ "http://es-1-1:9200" ]
```
- /volume5/storage/docker-data/logstash/conf/logstash-spring.conf
```text
input {
  file {
    path => "/app/log/*/*.json"
    codec => "json"
    start_position => beginning
  }
}

output {
  elasticsearch {
    hosts => ["http://es-1-1:9200"]
    index => "%{service}-%{+YYYY.MM.dd}"
    user => "admin"
    password => "***REMOVED***"
  }
}
```

# docker-compose
```shell
docker-compose --project-name logstash --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:
  logstash:
    image: logstash:7.17.10
    container_name: logstash
    hostname: logstash
    privileged: true
    user: root
    volumes:
      - /volume1/storage/docker-data/logstash/data/:/usr/share/logstash/data/
      - /volume1/storage/docker-data/logstash/conf/logstash.yml:/usr/share/logstash/config/logstash.yml
      - /volume1/storage/docker-data/logstash/conf/pipeline/:/usr/share/logstash/pipeline/
      - /volume1/storage/docker-data/app/log/:/app/log/
    restart: always
```