#!/bin/bash

DB_USERNAME={{ param_db_mysql_username }}
DB_PASSWORD={{ param_db_mysql_password }}

databases=$(docker exec mysql mysql --default-character-set=utf8mb4 -u$DB_USERNAME -p$DB_PASSWORD --skip-column-names -s -e 'SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME NOT IN ("mysql", "performance_schema","information_schema","sys","elu") ORDER BY `SCHEMA_NAME` ASC' | xargs)

DB_BACKUP_DIR=/volume2/backup/mysql

mkdir -p $DB_BACKUP_DIR

for t in $databases;do
  echo "mysql backuping $t"
  docker exec mysql mysqldump --default-character-set=utf8mb4 -u$DB_USERNAME -p$DB_PASSWORD --databases $t | gzip > $DB_BACKUP_DIR/$t.gz
done

scp -r $DB_BACKUP_DIR dsm:/volume1/public/backup/