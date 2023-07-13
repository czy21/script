# dockerfile

# docker-compose
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