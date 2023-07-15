
## dockerfile
- Dockerfile
```bash
docker build --tag registry.czy21-public.com/library/confluence --file Dockerfile . --pull
```
```dockerfile
FROM cptactionhank/atlassian-confluence:latest

USER root

COPY ./___temp/atlassian-agent.jar /opt/atlassian/confluence/
COPY ./___temp/lib/ /opt/atlassian/confluence/lib/

RUN echo 'export CATALINA_OPTS="-javaagent:/opt/atlassian/confluence/atlassian-agent.jar ${CATALINA_OPTS}"' >> /opt/atlassian/confluence/bin/setenv.sh
```
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