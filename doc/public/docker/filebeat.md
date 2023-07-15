
## conf
- /volume5/storage/docker-data/filebeat/conf/filebeat.yml
```text
filebeat.config:
  modules:
    path: ${path.config}/modules.d/*.yml
    reload.enabled: false

filebeat.autodiscover:
  providers:
    - type: docker
      hints.enabled: true

processors:
- add_cloud_metadata: ~

output.elasticsearch:
  hosts: '${ELASTICSEARCH_HOSTS}'
  username: '${ELASTICSEARCH_USERNAME}'
  password: '${ELASTICSEARCH_PASSWORD}'
  indices:
    - index: "docker--log-%{+yyyy.MM.dd}"
```
## docker-compose
```bash
docker-compose --project-name filebeat --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  filebeat:
    image: elastic/filebeat:7.17.9
    container_name: filebeat
    privileged: true
    user: root
    volumes:
      - /volume5/storage/docker-data/filebeat/conf/filebeat.yml:/usr/share/filebeat/filebeat.yml
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /volume5/docker-root/containers/:/var/lib/docker/containers:ro
    environment:
      ELASTICSEARCH_HOSTS: "<domain>:80"
      ELASTICSEARCH_USERNAME: "<username>"
      ELASTICSEARCH_PASSWORD: "<password>"
    restart: always
```