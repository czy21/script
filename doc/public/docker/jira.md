# dockerfile

# docker-compose
```yaml
version: "3.9"

services:
  jira:
    image: registry.czy21-internal.com/library/jira
    container_name: jira
    privileged: true
    user: root
    volumes:
      - /volume1/storage/docker-data/jira/data/:/var/atlassian/jira/
      - /volume1/storage/docker-data/jira/logs/:/opt/atlassian/jira/logs/
    environment:
      TZ: Asia/Shanghai
      CATALINA_OPTS: "-Xmx2G"




```