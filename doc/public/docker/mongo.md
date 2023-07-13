# dockerfile

# docker-compose
```yaml
version: "3.9"

services:

  mongo:
    image: mongo:4.4.19
    container_name: mongo
    privileged: true
    user: root
    ports:
      - "27017:27017"
    volumes:
      - /volume1/storage/docker-data/mongo/data/:/data/db/
      - /volume1/storage/docker-data/mongo/conf/:/data/configdb/
    environment:
      TZ: Asia/Shanghai
      MONGO_INITDB_ROOT_USERNAME: "<username>"
      MONGO_INITDB_ROOT_PASSWORD: "<password>"
    restart: always
```