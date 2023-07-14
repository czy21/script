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