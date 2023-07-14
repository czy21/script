## conf
- /volume5/storage/docker-data/rabbitmq/conf/enabled_plugins
```text
[rabbitmq_management,rabbitmq_prometheus,rabbitmq_mqtt].
```
## docker-compose
```bash
docker-compose --project-name rabbitmq --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:
  rabbitmq:
    image: rabbitmq:3.11.16-management-alpine
    container_name: rabbitmq
    privileged: true
    user: root
    expose:
      - "5672"
      - "15672"
      - "1883"
    ports:
      - "5672:5672"
      - "1883:1883"
    volumes:
      - /volume5/storage/docker-data/rabbitmq/conf/enabled_plugins:/etc/rabbitmq/enabled_plugins
      - /volume5/storage/docker-data/rabbitmq/data/:/var/lib/rabbitmq/
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: "<password>"
```