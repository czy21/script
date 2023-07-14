# dockerfile

# docker-compose
```shell
docker-compose --project-name node-exporter --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  node-exporter:
    image: prom/node-exporter
    container_name: node-exporter
    network_mode: host
    ports:
      - "9100:9100"
    volumes:
      - '/:/host:ro,rslave'
    command:
      - '--path.rootfs=/host'
    restart: always
```