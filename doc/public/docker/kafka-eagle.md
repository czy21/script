
## dockerfile
- Dockerfile
```bash
docker build --tag registry.czy21-public.com/library/kafka-eagle --file Dockerfile . --pull
```
```dockerfile
FROM openjdk:11-jdk

ENV KE_VERSION=3.0.1
ENV KE_TGZ_URL=https://github.com/smartloli/kafka-eagle-bin/raw/v${KE_VERSION}/efak-web-${KE_VERSION}-bin.tar.gz

ENV KE_HOME=/opt/kafka-eagle
ENV PATH=$KE_HOME/bin:$PATH

RUN mkdir -p $KE_HOME
#COPY ___temp/efak-web-${KE_VERSION}-bin.tar.gz $KE_HOME/src.gz
RUN wget -nv -O $KE_HOME/src.gz $KE_TGZ_URL;
RUN tar -xf $KE_HOME/src.gz --strip-components=1 -C $KE_HOME && rm $KE_HOME/src.gz && chown -R root:root $KE_HOME

WORKDIR $KE_HOME

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
```
## conf
- /volume5/storage/docker-data/kafka-eagle/conf/system-config.properties
```text
######################################
# multi zookeeper & kafka cluster list
# Settings prefixed with 'kafka.eagle.' will be deprecated, use 'efak.' instead
######################################
efak.zk.cluster.alias=cluster1
cluster1.zk.list=<ip>:2181,<ip>:2182,<ip>:2183/kafka/cluster1

######################################
# zookeeper enable acl
######################################
cluster1.zk.acl.enable=false
cluster1.zk.acl.schema=digest
cluster1.zk.acl.username=test
cluster1.zk.acl.password=test123

######################################
# broker size online list
######################################
cluster1.efak.broker.size=20

######################################
# zk client thread limit
######################################
kafka.zk.limit.size=16

######################################
# EFAK webui port
######################################
efak.webui.port=8048

######################################
# EFAK enable distributed
######################################
efak.distributed.enable=false
efak.cluster.mode.status=master
efak.worknode.master.host=localhost
efak.worknode.port=8085

######################################
# kafka jmx acl and ssl authenticate
######################################
cluster1.efak.jmx.acl=false
cluster1.efak.jmx.user=keadmin
cluster1.efak.jmx.password=keadmin123
cluster1.efak.jmx.ssl=false
cluster1.efak.jmx.truststore.location=/data/ssl/certificates/kafka.truststore
cluster1.efak.jmx.truststore.password=ke123456

######################################
# kafka offset storage
######################################
cluster1.efak.offset.storage=kafka
cluster2.efak.offset.storage=zk

######################################
# kafka jmx uri
######################################
cluster1.efak.jmx.uri=service:jmx:rmi:///jndi/rmi://%s/jmxrmi

######################################
# kafka metrics, 15 days by default
######################################
efak.metrics.charts=true
efak.metrics.retain=15

######################################
# kafka sql topic records max
######################################
efak.sql.topic.records.max=5000
efak.sql.topic.preview.records.max=10

######################################
# delete kafka topic token
######################################
efak.topic.token=keadmin

######################################
# kafka sasl authenticate
######################################
cluster1.efak.sasl.enable=false
cluster1.efak.sasl.protocol=SASL_PLAINTEXT
cluster1.efak.sasl.mechanism=SCRAM-SHA-256
cluster1.efak.sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required username="kafka" password="kafka-eagle";
cluster1.efak.sasl.client.id=
cluster1.efak.blacklist.topics=
cluster1.efak.sasl.cgroup.enable=false
cluster1.efak.sasl.cgroup.topics=
cluster2.efak.sasl.enable=false
cluster2.efak.sasl.protocol=SASL_PLAINTEXT
cluster2.efak.sasl.mechanism=PLAIN
cluster2.efak.sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="kafka" password="kafka-eagle";
cluster2.efak.sasl.client.id=
cluster2.efak.blacklist.topics=
cluster2.efak.sasl.cgroup.enable=false
cluster2.efak.sasl.cgroup.topics=

######################################
# kafka sqlite jdbc driver address
######################################
#efak.driver=org.sqlite.JDBC
#efak.url=jdbc:sqlite:/hadoop/kafka-eagle/db/ke.db
#efak.username=root
#efak.password=www.kafka-eagle.org

######################################
# kafka mysql jdbc driver address
######################################
efak.driver=com.mysql.cj.jdbc.Driver
efak.url=jdbc:mysql://<ip>:3306/ke?useUnicode=true&characterEncoding=UTF-8&zeroDateTimeBehavior=convertToNull
efak.username=<username>
efak.password=<password>
```
## docker-compose
```bash
docker-compose --project-name kafka-eagle --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.kafka-eagle.service: kafka-eagle
  traefik.http.services.kafka-eagle.loadbalancer.server.port: 8048

services:
  kafka-eagle:
    image: registry.czy21-public.com/library/kafka-eagle
    pull_policy: always
    container_name: kafka-eagle
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "8048"
    volumes:
      - /volume5/storage/docker-data/kafka-eagle/conf/system-config.properties:/opt/kafka-eagle/conf/system-config.properties
      - /volume5/storage/docker-data/kafka-eagle/logs/:/opt/kafka-eagle/logs/
    restart: always
```