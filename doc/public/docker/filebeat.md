# dockerfile

# docker-compose
```yaml
version: "3.9"

services:

  filebeat:
    image: elastic/filebeat:7.17.9
    container_name: filebeat
    privileged: true
    user: root
    volumes:
      - /volume1/storage/docker-data/filebeat/conf/filebeat.yml:/usr/share/filebeat/filebeat.yml
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /volume1/docker-root/containers/:/var/lib/docker/containers:ro
    environment:
      ELASTICSEARCH_HOSTS: "<domain>:80"
      ELASTICSEARCH_USERNAME: "<username>"
      ELASTICSEARCH_PASSWORD: "<password>"
    restart: always
```