#!/bin/bash


DB_USERNAME={{ param_db_pgsql_username }}
DB_PASSWORD={{ param_db_pgsql_password }}

CLI="docker run --rm postgres:14.18-alpine"

DB_BACKUP_DIR=$1/pgsql

mkdir -p $DB_BACKUP_DIR

function backup(){

  local host=$1
  local port=$2

  ${CLI} psql postgresql://$DB_USERNAME:$DB_PASSWORD@$host:$port -c "\conninfo"

  if [ $? -ne 0 ];then
    return
  fi

  databases=$(${CLI} psql postgresql://$DB_USERNAME:$DB_PASSWORD@$host:$port -c "select datname from pg_database where datname not in ('postgres') and datname not like 'template%' order by datname asc" --pset=tuples_only=on | xargs)
  
  for t in $databases;do
    echo "pgsql backup $host:$port => $t"
    ${CLI} pg_dump postgresql://$DB_USERNAME:$DB_PASSWORD@$host:$port/$t | gzip > $DB_BACKUP_DIR/$host-$port-$t.gz
  done
}

backup db.czy21.com 5432
backup db02.czy21.com 5432