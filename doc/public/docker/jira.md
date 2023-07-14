
## docker-compose
```bash
docker-compose --project-name jira --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:
  jira:
    image: registry.czy21-public.com/library/jira
    container_name: jira
    privileged: true
    user: root
    volumes:
      - /volume5/storage/docker-data/jira/data/:/var/atlassian/jira/
      - /volume5/storage/docker-data/jira/logs/:/opt/atlassian/jira/logs/
    environment:
      TZ: Asia/Shanghai
      CATALINA_OPTS: "-Xmx2G"




```