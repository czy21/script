#!/bin/bash

DB_USERNAME={{ param_db_pgsql_username }}
DB_PASSWORD={{ param_db_pgsql_password }}

databases=$(docker exec -e PGPASSWORD=$DB_PASSWORD pgsql psql --username=$DB_USERNAME -c "select datname from pg_database where datname not in ('postgres') and datname not like 'template%' order by datname asc" --pset=tuples_only=on | xargs)

DB_BACKUP_DIR=/volume2/backup/pgsql

mkdir -p $DB_BACKUP_DIR

for t in $databases;do
  echo "pgsql backuping $t"
  docker exec -e PGPASSWORD=$DB_PASSWORD pgsql pg_dump --username=$DB_USERNAME --dbname=$t | gzip > $DB_BACKUP_DIR/$t.gz
done

scp -r $DB_BACKUP_DIR dsm:/volume1/public/backup/