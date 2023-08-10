
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/nexus-pro --file Dockerfile . --pull
```
```dockerfile
FROM openjdk:8-jdk
ENV SONATYPE_WORK=/sonatype-work
ENV NEXUS_HOME=/opt/sonatype/nexus
COPY sources.list /etc/apt/
COPY ./___temp/nexus-oss.tar.gz $NEXUS_HOME/src.tgz
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

RUN mkdir -p ${NEXUS_HOME} && tar -xf $NEXUS_HOME/src.tgz --strip-components=1 -C $NEXUS_HOME && rm $NEXUS_HOME/src.tgz

RUN useradd -r -u 200 -m -c "nexus role account" -d ${SONATYPE_WORK} -s /bin/false nexus

WORKDIR ${NEXUS_HOME}
USER nexus

ENV CONTEXT_PATH /nexus
ENV MAX_HEAP 768m
ENV MIN_HEAP 256m
ENV JAVA_OPTS -server -Djava.net.preferIPv4Stack=true
ENV LAUNCHER_CONF ./conf/jetty.xml ./conf/jetty-requestlog.xml ./conf/jetty-http.xml

VOLUME ${SONATYPE_WORK}

EXPOSE 8081
ENTRYPOINT ["/docker-entrypoint.sh"]
```
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