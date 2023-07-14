
## dockerfile
- DockerfileBase
```bash
docker build --tag registry.czy21-public.com/library/hadoop-base --file DockerfileBase . --pull
```
```dockerfile
FROM openjdk:8-jdk

# hadoop
ENV HADOOP_VERSION=3.3.4
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$HADOOP_HOME/bin:$PATH
RUN set -ex; \
    mkdir -p $HADOOP_HOME $HADOOP_HOME/hdfs/name/ $HADOOP_HOME/hdfs/data/; \
    wget -nv -O $HADOOP_HOME/src.tgz https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz; \
    tar -xf $HADOOP_HOME/src.tgz --strip-components=1 -C $HADOOP_HOME; \
    rm $HADOOP_HOME/src.tgz; \
    chown -R root:root $HADOOP_HOME;

RUN rm -rf $HADOOP_HOME/share/doc/;

# hbase
ENV HBASE_VERSION=2.5.0
ENV HBASE_HOME=/opt/hbase
ENV PATH=$HBASE_HOME/bin:$PATH
RUN set -ex; \
    mkdir -p $HBASE_HOME; \
    wget -nv -O $HBASE_HOME/src.tgz https://archive.apache.org/dist/hbase/${HBASE_VERSION}/hbase-${HBASE_VERSION}-bin.tar.gz; \
    tar -xf $HBASE_HOME/src.tgz --strip-components=1 -C $HBASE_HOME; \
    rm $HBASE_HOME/src.tgz; \
    chown -R root:root $HBASE_HOME;

RUN rm -rf $HBASE_HOME/docs/;

ARG SSH_PUB='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com'
# RUN sed -i.bak "s,\(security\|deb\).debian.org,<ip|domain>/repository/apt-proxy,g" /etc/apt/sources.list
RUN apt-get update;
RUN apt-get install -y openssh-server net-tools vim git;
RUN sed -i -r 's/^\s*UseDNS\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/' /etc/ssh/sshd_config;
RUN echo 'UseDNS no \nPermitRootLogin yes \nPasswordAuthentication yes \nClientAliveInterval 30' >> /etc/ssh/sshd_config;
RUN cat /etc/ssh/sshd_config
RUN su root bash -c 'cd;mkdir .ssh;chmod 700 .ssh;echo ${SSH_PUB} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys'
RUN su root bash -c 'cd;ssh-keygen -t rsa -f ~/.ssh/id_rsa; cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys'
```
- Dockerfile
```bash
docker build --tag registry.czy21-public.com/library/hadoop --file Dockerfile . --pull
```
```dockerfile
FROM registry.czy21-internal.com/library/hadoop-base

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
EXPOSE 22 9870 9000
ENTRYPOINT ["/docker-entrypoint.sh"]
```
## conf
- /volume5/storage/docker-data/hadoop/conf/core-site.xml
```text
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://hadoop-namenode:9000</value>
    </property>
    <property>
        <name>dfs.namenode.rpc-bind-host</name>
        <value>0.0.0.0</value>
    </property>
</configuration>
```
- /volume5/storage/docker-data/hadoop/conf/hadoop-env.sh
```text
export HDFS_DATANODE_USER=root
export HDFS_NAMENODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export JAVA_HOME=/usr/local/openjdk-8
export HADOOP_OS_TYPE=${HADOOP_OS_TYPE:-$(uname -s)}
export HADOOP_OPTS="-Djava.library.path=${HADOOP_HOME}/lib/native"
```
- /volume5/storage/docker-data/hadoop/conf/hdfs-site.xml
```text
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///opt/hadoop/hdfs/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///opt/hadoop/hdfs/data</value>
    </property>

    <property>
        <name>dfs.permissions</name>
        <value>false</value>
    </property>

    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
```
## docker-compose
```bash
docker-compose --project-name hadoop --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:
  hadoop-namenode:
    image: 'registry.czy21-public.com/library/hadoop'
    container_name: 'hadoop-namenode'
    hostname: 'hadoop-namenode'
    ports:
      - "9870:9870"
    volumes:
      - '/volume5/storage/docker-data/hadoop/conf/hadoop-env.sh:/opt/hadoop/etc/hadoop/hadoop-env.sh'
      - '/volume5/storage/docker-data/hadoop/conf/core-site.xml:/opt/hadoop/etc/hadoop/core-site.xml'
      - '/volume5/storage/docker-data/hadoop/conf/hdfs-site.xml:/opt/hadoop/etc/hadoop/hdfs-site.xml'
      - '/volume5/storage/docker-data/hadoop/data/namenode/:/opt/hadoop/hdfs/'
    environment:
      HADOOP_NODE_TYPE: namenode
  
  hadoop-datanode-1:
    image: 'registry.czy21-public.com/library/hadoop'
    container_name: 'hadoop-datanode-1'
    hostname: 'hadoop-datanode-1'
    volumes:
      - '/volume5/storage/docker-data/hadoop/conf/hadoop-env.sh:/opt/hadoop/etc/hadoop/hadoop-env.sh'
      - '/volume5/storage/docker-data/hadoop/conf/core-site.xml:/opt/hadoop/etc/hadoop/core-site.xml'
      - '/volume5/storage/docker-data/hadoop/conf/hdfs-site.xml:/opt/hadoop/etc/hadoop/hdfs-site.xml'
      - '/volume5/storage/docker-data/hadoop/data/datanode/1:/opt/hadoop/hdfs/'
    environment:
      HADOOP_NODE_TYPE: datanode
  
  hadoop-datanode-2:
    image: 'registry.czy21-public.com/library/hadoop'
    container_name: 'hadoop-datanode-2'
    hostname: 'hadoop-datanode-2'
    volumes:
      - '/volume5/storage/docker-data/hadoop/conf/hadoop-env.sh:/opt/hadoop/etc/hadoop/hadoop-env.sh'
      - '/volume5/storage/docker-data/hadoop/conf/core-site.xml:/opt/hadoop/etc/hadoop/core-site.xml'
      - '/volume5/storage/docker-data/hadoop/conf/hdfs-site.xml:/opt/hadoop/etc/hadoop/hdfs-site.xml'
      - '/volume5/storage/docker-data/hadoop/data/datanode/2:/opt/hadoop/hdfs/'
    environment:
      HADOOP_NODE_TYPE: datanode
  
```