# dockerfile

# docker-compose
```yaml
version: "3.9"

services:
  hadoop-namenode:
    image: 'registry.czy21-internal.com/library/hadoop'
    container_name: 'hadoop-namenode'
    hostname: 'hadoop-namenode'
    ports:
      - "9870:9870"
    volumes:
      - '/volume1/storage/docker-data/hadoop/conf/hadoop-env.sh:/opt/hadoop/etc/hadoop/hadoop-env.sh'
      - '/volume1/storage/docker-data/hadoop/conf/core-site.xml:/opt/hadoop/etc/hadoop/core-site.xml'
      - '/volume1/storage/docker-data/hadoop/conf/hdfs-site.xml:/opt/hadoop/etc/hadoop/hdfs-site.xml'
      - '/volume1/storage/docker-data/hadoop/data/namenode/:/opt/hadoop/hdfs/'
    environment:
      HADOOP_NODE_TYPE: namenode
  
  hadoop-datanode-1:
    image: 'registry.czy21-internal.com/library/hadoop'
    container_name: 'hadoop-datanode-1'
    hostname: 'hadoop-datanode-1'
    volumes:
      - '/volume1/storage/docker-data/hadoop/conf/hadoop-env.sh:/opt/hadoop/etc/hadoop/hadoop-env.sh'
      - '/volume1/storage/docker-data/hadoop/conf/core-site.xml:/opt/hadoop/etc/hadoop/core-site.xml'
      - '/volume1/storage/docker-data/hadoop/conf/hdfs-site.xml:/opt/hadoop/etc/hadoop/hdfs-site.xml'
      - '/volume1/storage/docker-data/hadoop/data/datanode/1:/opt/hadoop/hdfs/'
    environment:
      HADOOP_NODE_TYPE: datanode
  
  hadoop-datanode-2:
    image: 'registry.czy21-internal.com/library/hadoop'
    container_name: 'hadoop-datanode-2'
    hostname: 'hadoop-datanode-2'
    volumes:
      - '/volume1/storage/docker-data/hadoop/conf/hadoop-env.sh:/opt/hadoop/etc/hadoop/hadoop-env.sh'
      - '/volume1/storage/docker-data/hadoop/conf/core-site.xml:/opt/hadoop/etc/hadoop/core-site.xml'
      - '/volume1/storage/docker-data/hadoop/conf/hdfs-site.xml:/opt/hadoop/etc/hadoop/hdfs-site.xml'
      - '/volume1/storage/docker-data/hadoop/data/datanode/2:/opt/hadoop/hdfs/'
    environment:
      HADOOP_NODE_TYPE: datanode
  
```