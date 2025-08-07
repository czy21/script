#!/bin/bash


DB_USERNAME={{ param_db_mysql_username }}
DB_PASSWORD={{ param_db_mysql_password }}

CLI="docker run --rm mysql:8.4.0"

DB_BACKUP_DIR=$1/mysql

mkdir -p $DB_BACKUP_DIR

function backup(){

  local host=$1
  local port=$2

  ${CLI} mysql --default-character-set=utf8mb4 -h$host -p$port -u$DB_USERNAME -p$DB_PASSWORD -e 'STATUS'
  
  if [ $? -ne 0 ];then
    return
  fi

  databases=$(${CLI} mysql --default-character-set=utf8mb4 -h$host -p$port -u$DB_USERNAME -p$DB_PASSWORD --skip-column-names -s -e 'SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME NOT IN ("mysql", "performance_schema","information_schema","sys","elu") ORDER BY `SCHEMA_NAME` ASC' | xargs)
  
  for t in $databases;do
    echo "mysql backup $host:$port => $t"
    ${CLI} mysqldump --default-character-set=utf8mb4 -h$host -p$port -u$DB_USERNAME -p$DB_PASSWORD --databases $t | gzip > $DB_BACKUP_DIR/$host-$port-$t.gz
  done
}

backup db.czy21.com 3306
backup db02.czy21.com 3306