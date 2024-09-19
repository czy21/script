#!/bin/bash

# https://learn.microsoft.com/zh-cn/sql/linux/sql-server-linux-backup-and-restore-database?view=sql-server-ver16

DB_USERNAME={{ param_db_mssql_username }}
DB_PASSWORD={{ param_db_mssql_password }}

databases=$(docker exec mssql /opt/mssql-tools/bin/sqlcmd -U $DB_USERNAME -P $DB_PASSWORD -Q "set nocount on;select name from sys.databases where name not in ('master','model','msdb','tempdb')" -h -1 | xargs)

DB_BACKUP_DIR=$1/mssql

mkdir -p $DB_BACKUP_DIR

for t in $databases;do
  echo "mssql backuping $t"
  docker exec mssql /opt/mssql-tools/bin/sqlcmd -U $DB_USERNAME -P $DB_PASSWORD -Q "BACKUP DATABASE [$t] TO DISK = N'/var/opt/mssql/backup/$t.bak'"
  docker cp mssql:/var/opt/mssql/backup/$t.bak $DB_BACKUP_DIR
  docker exec mssql rm -vrf /var/opt/mssql/backup/$t.bak
done