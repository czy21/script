# dockerfile

# docker-compose
```yaml
version: "3.9"

services:

  db:
    image: neo4j:4.4
    container_name: neo4j
    privileged: true
    user: root
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - /volume1/storage/docker-data/neo4j/data/:/data/
      - /volume1/storage/docker-data/neo4j/data/logs:/logs/
      - /volume1/storage/docker-data/neo4j/conf/:/conf/
    environment:
      NEO4J_AUTH: neo4j/<password>
      NEO4J_dbms_memory_pagecache_size: 2g


```