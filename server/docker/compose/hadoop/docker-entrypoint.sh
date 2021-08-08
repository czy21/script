#!/bin/bash
set -e

service ssh start

$HADOOP_HOME/bin/hdfs namenode -format
$HADOOP_HOME/sbin/start-dfs.sh

$HBASE_HOME/bin/start-hbase.sh

exec "$@"