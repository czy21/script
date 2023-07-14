
## conf
- /volume5/storage/docker-data/mongo/conf/mongod.conf
```text
# mongod.conf

# for documentation of all options, see:
#   http://docs.mongodb.org/manual/reference/configuration-options/

# Where and how to store data.
storage:
  dbPath: /data/db
  journal:
    enabled: true
#  engine:
#  mmapv1:
#  wiredTiger:

# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /data/configdb/mongod.log

# network interfaces
net:
  port: 27017
  bindIp: 0.0.0.0

# how the process runs
processManagement:
  timeZoneInfo: /usr/share/zoneinfo

#security:
#  authorization: enabled

#operationProfiling:

#replication:

#sharding:

## Enterprise-Only Options:

#auditLog:

#snmp:
```
## docker-compose
```bash
docker-compose --project-name mongo --file docker-compose.yaml up --detach --build --remove-orphans
```
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
      - /volume5/storage/docker-data/mongo/data/:/data/db/
      - /volume5/storage/docker-data/mongo/conf/:/data/configdb/
    environment:
      TZ: Asia/Shanghai
      MONGO_INITDB_ROOT_USERNAME: "<username>"
      MONGO_INITDB_ROOT_PASSWORD: "<password>"
    restart: always
```