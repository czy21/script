# dockerfile

# docker-compose
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