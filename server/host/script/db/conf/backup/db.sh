#!/bin/bash
CURRENT_DIR=$(cd "$(dirname "$0")"; pwd)

DB_BACKUP_DIR=/volume2/@team/backup/db

source=$(find $CURRENT_DIR -name 'db-*.sh' -exec sh -c 'f={}; echo "${f#*db-}" | sed "s|\.sh$||"' \;)

target=
while getopts "t:c" opt;do
    case $opt in
        t) target=$OPTARG;;
    esac
done;

target=$(echo $target | tr ',' ' ')

[ -z "$target" ] && target=$source

for t in $target;do
  bash $CURRENT_DIR/db-${t}.sh "$DB_BACKUP_DIR"
done