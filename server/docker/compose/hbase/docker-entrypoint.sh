#!/bin/bash
set -e

service ssh start

$HBASE_HOME/bin/start-hbase.sh
exec "$@"