#!/bin/bash
set -e

service ssh start

# start hbase
$HBASE_HOME/bin/start-hbase.sh
exec "$@"