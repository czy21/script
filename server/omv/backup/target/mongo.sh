#!/bin/bash

# https://learn.microsoft.com/zh-cn/sql/linux/sql-server-linux-backup-and-restore-database?view=sql-server-ver16

DB_USERNAME={{ param_db_mongo_username }}
DB_PASSWORD={{ param_db_mongo_password }}

databases=$(docker exec mongo mongo mongodb://$DB_USERNAME:$DB_PASSWORD@127.0.0.1:27017/?authSource=admin --eval 'db.adminCommand({ listDatabases: 1, nameOnly: true,filter: {"name":{$nin:["demo","config","local"]}}})' --quiet | xargs)

DB_BACKUP_DIR=/volume2/backup/mongo

mkdir -p $DB_BACKUP_DIR

for t in $databases;do
  echo "mongo backuping $t"
done

# scp -r $DB_BACKUP_DIR dsm:/volume1/public/backup/