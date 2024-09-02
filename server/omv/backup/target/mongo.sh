#!/bin/bash

# https://learn.microsoft.com/zh-cn/sql/linux/sql-server-linux-backup-and-restore-database?view=sql-server-ver16

DB_USERNAME={{ param_db_mongo_username }}
DB_PASSWORD={{ param_db_mongo_password }}

databases=$(docker exec mongo mongo mongodb://$DB_USERNAME:$DB_PASSWORD@127.0.0.1:27017/?authSource=admin --eval 'db.adminCommand({ listDatabases: 1,filter: {"name":{$nin:["admin","config","local"]}}}).databases.map(t=>t.name).join(" ")' --quiet | xargs)

DB_BACKUP_DIR=/volume2/backup/mongo

mkdir -p $DB_BACKUP_DIR

for t in $databases;do
  echo "mongo backuping $t"
  docker exec mongo mongodump --uri=mongodb://$DB_USERNAME:$DB_PASSWORD@127.0.0.1:27017/?authSource=admin --db=$t --archive --gzip > $DB_BACKUP_DIR/$t.gz
done

scp -r $DB_BACKUP_DIR dsm:/volume1/public/backup/