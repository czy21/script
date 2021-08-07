#!/bin/bash
set -e

service ssh start
# start hadoop
$HADOOP_HOME/bin/hdfs namenode -format
$HADOOP_HOME/sbin/start-dfs.sh

# start hbase
$HBASE_HOME/bin/start-hbase.sh
exec "$@"