
## docker-compose
```bash
docker-compose --project-name zk --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"
  
  
  

services:
  zk-1:
    image: zookeeper:3.8.0
    container_name: zk-1
    ports:
      - 2181:2181
    volumes:
      - /volume5/storage/docker-data/zk/data/1:/data/
      - /volume5/storage/docker-data/zk/datalog/1:/datalog/
      - /volume5/storage/docker-data/zk/logs/1:/logs/
    environment:
      ZOO_MY_ID: 1
      ZOO_TICK_TIME: 60000
      ZOO_SERVERS: server.1=zk-1:2888:3888;2181 server.2=zk-2:2888:3888;2181 server.3=zk-3:2888:3888;2181
    restart: always
  zk-2:
    image: zookeeper:3.8.0
    container_name: zk-2
    ports:
      - 2182:2181
    volumes:
      - /volume5/storage/docker-data/zk/data/2:/data/
      - /volume5/storage/docker-data/zk/datalog/2:/datalog/
      - /volume5/storage/docker-data/zk/logs/2:/logs/
    environment:
      ZOO_MY_ID: 2
      ZOO_TICK_TIME: 60000
      ZOO_SERVERS: server.1=zk-1:2888:3888;2181 server.2=zk-2:2888:3888;2181 server.3=zk-3:2888:3888;2181
    restart: always
  zk-3:
    image: zookeeper:3.8.0
    container_name: zk-3
    ports:
      - 2183:2181
    volumes:
      - /volume5/storage/docker-data/zk/data/3:/data/
      - /volume5/storage/docker-data/zk/datalog/3:/datalog/
      - /volume5/storage/docker-data/zk/logs/3:/logs/
    environment:
      ZOO_MY_ID: 3
      ZOO_TICK_TIME: 60000
      ZOO_SERVERS: server.1=zk-1:2888:3888;2181 server.2=zk-2:2888:3888;2181 server.3=zk-3:2888:3888;2181
    restart: always


```