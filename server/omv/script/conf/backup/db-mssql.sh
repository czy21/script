#!/bin/bash

# https://learn.microsoft.com/zh-cn/sql/linux/sql-server-linux-backup-and-restore-database?view=sql-server-ver16
DB_USERNAME={{ param_db_mssql_username }}
DB_PASSWORD={{ param_db_mssql_password }}

CLI="docker run --rm mssql/server:2022-latest"

DB_BACKUP_DIR=$1/mssql

mkdir -p $DB_BACKUP_DIR

function backup(){

  local host=$1
  local port=$2

  ${CLI} /opt/mssql-tools/bin/sqlcmd -S $host,$port -U $DB_USERNAME -P $DB_PASSWORD -Q "select 1" -h -1

  if [ $? -ne 0 ];then
    return
  fi

  databases=$(${CLI} /opt/mssql-tools/bin/sqlcmd -S $host,$port -U $DB_USERNAME -P $DB_PASSWORD -Q "set nocount on;select name from sys.databases where name not in ('master','model','msdb','tempdb')" -h -1 | sed '1,3d' | xargs)
  
  for t in $databases;do
    echo "mssql backup $host:$port => $t"
    # ${CLI} /opt/mssql-tools/bin/sqlcmd -S $host,$port -U $DB_USERNAME -P $DB_PASSWORD -Q "BACKUP DATABASE [$t] TO DISK = N'/dev/stdout'" | gzip > $DB_BACKUP_DIR/$host-$port-$t.gz
  done
}

backup db.czy21.com 1433