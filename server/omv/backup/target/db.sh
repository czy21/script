#!/bin/bash
CURRENT_DIR=$(cd "$(dirname "$0")"; pwd)

DB_BACKUP_DIR=/volume2/backup/db

sh $CURRENT_DIR/mysql.sh "$DB_BACKUP_DIR"
sh $CURRENT_DIR/pgsql.sh "$DB_BACKUP_DIR"
sh $CURRENT_DIR/mssql.sh "$DB_BACKUP_DIR"
sh $CURRENT_DIR/mongo.sh "$DB_BACKUP_DIR"