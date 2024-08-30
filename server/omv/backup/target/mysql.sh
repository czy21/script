#!/bin/bash

MYSQL_USERNAME={{ param_db_mysql_username }}
MYSQL_PASSWORD={{ param_db_mysql_password }}

databases=$(docker exec mysql mysql --default-character-set=utf8mb4 -u$MYSQL_USERNAME -p$MYSQL_PASSWORD --skip-column-names -s -e 'SHOW DATABASES WHERE `Database` NOT IN ("mysql", "performance_schema","information_schema","sys","elu")' | xargs)

MYSQL_BACKUP_DIR=/volume2/backup/mysql

mkdir -p $MYSQL_BACKUP_DIR

for t in $databases;do
  echo "backuping $t"
  docker exec mysql mysqldump --default-character-set=utf8mb4 --databases $t -u$MYSQL_USERNAME -p$MYSQL_PASSWORD | gzip > $MYSQL_BACKUP_DIR/$t.gz
done

scp -r $MYSQL_BACKUP_DIR dsm:/volume1/public/backup/