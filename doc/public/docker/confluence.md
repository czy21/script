
## docker-compose
```bash
docker-compose --project-name confluence --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:
  confluence:
    image: registry.czy21-public.com/library/confluence
    container_name: confluence
    privileged: true
    user: root
    volumes:
      - /volume5/storage/docker-data/confluence/data/:/var/atlassian/confluence/
    environment:
      TZ: Asia/Shanghai
      CATALINA_OPTS: "-Xmx2G"




```