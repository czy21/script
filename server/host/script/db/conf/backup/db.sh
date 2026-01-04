#!/bin/bash
CURRENT_DIR=$(cd "$(dirname "$0")"; pwd)

DB_BACKUP_DIR=/volume2/@team/backup/db

bash $CURRENT_DIR/db-mysql.sh "$DB_BACKUP_DIR"
bash $CURRENT_DIR/db-pgsql.sh "$DB_BACKUP_DIR"
bash $CURRENT_DIR/db-mssql.sh "$DB_BACKUP_DIR"
bash $CURRENT_DIR/db-mongo.sh "$DB_BACKUP_DIR"