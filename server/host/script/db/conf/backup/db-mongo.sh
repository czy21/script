#!/bin/bash

# https://www.mongodb.com/zh-cn/docs/database-tools/mongodump/mongodump-examples/
DB_USERNAME={{ param_db_mongo_username }}
DB_PASSWORD={{ param_db_mongo_password }}

CLI="docker run --rm mongo:4.4.19"

DB_BACKUP_DIR=$1/mongo

mkdir -p $DB_BACKUP_DIR

function backup(){

  local host=$1
  local port=$2

  ${CLI} mongo mongodb://$DB_USERNAME:$DB_PASSWORD@$host:$port/?authSource=admin --eval 'db.runCommand({ping:1})'

  if [ $? -ne 0 ];then
    return
  fi

  databases=$(${CLI} mongo mongodb://$DB_USERNAME:$DB_PASSWORD@$host:$port/?authSource=admin --eval 'db.adminCommand({ listDatabases: 1,filter: {"name":{$nin:["admin","config","local"]}}}).databases.map(t=>t.name).join(" ")' --quiet | xargs)

  for t in $databases;do
    echo "mongo backup $host:$port => $t"
    ${CLI} mongodump --uri=mongodb://$DB_USERNAME:$DB_PASSWORD@$host:$port/?authSource=admin --db=$t --archive --gzip > $DB_BACKUP_DIR/$host-$port-$t.gz
  done
}

backup db.czy21.com 27017