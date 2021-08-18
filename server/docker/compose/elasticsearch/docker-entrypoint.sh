#!/bin/bash
set -e

service ssh start

#if [ $HBASE_NODE_TYPE = "master" ]; then
#  echo -e "\033[32m hbase master start \033[0m"
#  $HBASE_HOME/bin/hbase master start
#elif [ $HBASE_NODE_TYPE = "region" ]; then
#  echo -e "\033[32m hbase region start \033[0m"
#  $HBASE_HOME/bin/hbase regionserver start
#fi