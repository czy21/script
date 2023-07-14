
## docker-compose
```bash
docker-compose --project-name nexus-pro --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  nexus-pro:
    container_name: nexus-pro
    build:
      context: /home/opsor/docker/db/nexus-pro
      dockerfile: /home/opsor/docker/db/nexus-pro/Dockerfile
    privileged: true
    user: root
    ports:
      - "8090:8081"
    volumes:
      - /volume5/storage/docker-data/nexus-pro/data/:/sonatype-work/
    environment:
      TZ: Asia/Shanghai



```