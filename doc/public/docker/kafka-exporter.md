# dockerfile

# docker-compose
```shell
docker-compose --project-name kafka-exporter --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  kafka_exporter:
    image: danielqsj/kafka-exporter
    container_name: kafka_exporter
    ports:
      - "9308:9308"
    command: ["--kafka.server=:9092","--kafka.server=:9093"]

    user: root

```