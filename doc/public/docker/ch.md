# dockerfile

# docker-compose
```yaml
version: "3.9"

x-app-common: &app-common
  image: clickhouse/clickhouse-server:22.8

services:
  ch-1-1:
    <<: *app-common
    container_name: ch-1-1
    hostname: ch-1-1
    expose:
      - "8123"
      - "9000"
      - "9009"
      - "9004"
    ports:
      - '8124:8123'
    volumes:
      - '/volume1/storage/docker-data/ch-1/conf/config.xml:/etc/clickhouse-server/config.d/config.xml'
      - '/volume1/storage/docker-data/ch-1/conf/users.xml:/etc/clickhouse-server/users.d/users.xml'
      - '/volume1/storage/docker-data/ch-1/data/1:/var/lib/clickhouse/'
      - '/volume1/storage/docker-data/ch-1/data/1/data/:/var/lib/clickhouse/data/'
      - '/volume1/storage/docker-data/ch-1/log/1:/var/log/'
    environment:
      CLICKHOUSE_DB: default
      CLICKHOUSE_USER: <username>
      CLICKHOUSE_PASSWORD: <password>
      CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT: 1
  ch-1-2:
    <<: *app-common
    container_name: ch-1-2
    hostname: ch-1-2
    expose:
      - "8123"
      - "9000"
      - "9009"
      - "9004"
    ports:
      - '8125:8123'
    volumes:
      - '/volume1/storage/docker-data/ch-1/conf/config.xml:/etc/clickhouse-server/config.d/config.xml'
      - '/volume1/storage/docker-data/ch-1/conf/users.xml:/etc/clickhouse-server/users.d/users.xml'
      - '/volume1/storage/docker-data/ch-1/data/2:/var/lib/clickhouse/'
      - '/volume1/storage/docker-data/ch-1/data/2/data/:/var/lib/clickhouse/data/'
      - '/volume1/storage/docker-data/ch-1/log/2:/var/log/'
    environment:
      CLICKHOUSE_DB: default
      CLICKHOUSE_USER: <username>
      CLICKHOUSE_PASSWORD: <password>
      CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT: 1
```