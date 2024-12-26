#!/bin/bash
CURRENT_DIR=$(cd "$(dirname "$0")"; pwd)

DB_BACKUP_DIR=/volume2/backup/db

sh $CURRENT_DIR/db-mysql.sh "$DB_BACKUP_DIR"
sh $CURRENT_DIR/db-pgsql.sh "$DB_BACKUP_DIR"
sh $CURRENT_DIR/db-mssql.sh "$DB_BACKUP_DIR"
sh $CURRENT_DIR/db-mongo.sh "$DB_BACKUP_DIR"