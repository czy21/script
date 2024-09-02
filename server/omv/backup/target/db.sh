#!/bin/bash
CURRENT_DIR=$(cd "$(dirname "$0")"; pwd)

sh $CURRENT_DIR/mysql.sh
sh $CURRENT_DIR/pgsql.sh
sh $CURRENT_DIR/mssql.sh
sh $CURRENT_DIR/mongo.sh