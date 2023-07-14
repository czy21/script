# dockerfile
# conf
- /volume5/storage/docker-data/ch-1/conf/config.xml
```text
<?xml version="1.0"?>
<yandex>
    <listen_host>0.0.0.0</listen_host>
    <mysql_port>9004</mysql_port>
    <remote_servers>
        <ch-1>
            <shard>
                <replica>
                    <host>ch-1-1</host>
                    <port>9000</port>
                    <user>admin</user>
                    <password>***REMOVED***</password>
                </replica>
            </shard>
            <shard>
                <replica>
                    <host>ch-1-2</host>
                    <port>9000</port>
                    <user>admin</user>
                    <password>***REMOVED***</password>
                </replica>
            </shard>
        </ch-1>
    </remote_servers>

    <zookeeper>
        <node index="1">
            <host>192.168.2.18</host>
            <port>2181</port>
        </node>
    </zookeeper>

    <networks>
        <ip>::/0</ip>
    </networks>

    <macros>
        <shard>01</shard>
        <replica>ch-1-1</replica>
    </macros>

    <clickhouse_compression>
        <case>
            <min_part_size>10000000000</min_part_size>
            <min_part_size_ratio>0.01</min_part_size_ratio>
            <method>lz4</method>
        </case>
    </clickhouse_compression>

</yandex>
```
- /volume5/storage/docker-data/ch-1/conf/users.xml
```text
<?xml version="1.0"?>
<yandex>
    <users>
        <default>
            <password>***REMOVED***</password>
        </default>
    </users>
    <profiles>
      <max_partitions_per_insert_block>2000</max_partitions_per_insert_block>
    </profiles>
</yandex>
```

# docker-compose
```shell
docker-compose --project-name ch-1 --file docker-compose.yaml up --detach --build --remove-orphans
```
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
      CLICKHOUSE_USER: admin
      CLICKHOUSE_PASSWORD: ***REMOVED***
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
      CLICKHOUSE_USER: admin
      CLICKHOUSE_PASSWORD: ***REMOVED***
      CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT: 1
```