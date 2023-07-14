
## dockerfile
- Dockerfile
```bash
docker build --tag registry.czy21-public.com/library/jira --file Dockerfile . --pull
```
```dockerfile
FROM cptactionhank/atlassian-jira-software:latest

USER root

COPY ./___temp/atlassian-agent.jar /opt/atlassian/jira/
COPY ./___temp/lib/ /opt/atlassian/jira/lib/

RUN echo 'export CATALINA_OPTS="-javaagent:/opt/atlassian/jira/atlassian-agent.jar ${CATALINA_OPTS}"' >> /opt/atlassian/jira/bin/setenv.sh
```
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