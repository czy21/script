#!/bin/bash
set -e

service ssh start

hdfs_dir=$HADOOP_HOME/hdfs/

if [ "$(ls -A ${hdfs_dir})" ]; then
  echo -e "\033[32m hdfs is not empty \033[0m"
else
  echo -e "\033[32m hdfs namenode format... \033[0m"
  $HADOOP_HOME/bin/hdfs namenode -format
fi

echo -e "\033[32m start dfs... \033[0m"
$HADOOP_HOME/sbin/start-dfs.sh

echo -e "\033[32m start hbase... \033[0m"
$HBASE_HOME/bin/start-hbase.sh

exec "$@"