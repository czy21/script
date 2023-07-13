# dockerfile

# docker-compose
```yaml
version: "3.9"

services:
  confluence:
    image: registry.czy21-internal.com/library/confluence
    container_name: confluence
    privileged: true
    user: root
    volumes:
      - /volume1/storage/docker-data/confluence/data/:/var/atlassian/confluence/
    environment:
      TZ: Asia/Shanghai
      CATALINA_OPTS: "-Xmx2G"




```