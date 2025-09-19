#!/bin/bash

hostname=
username=
password=
repository=

while getopts "h:u:p:r:" opt;do
    case $opt in
        h) hostname=$OPTARG;;
        u) username=$OPTARG;;
        p) password=$OPTARG;;
        r) repository=$OPTARG;;
    esac
done;


while true; do
  components=`curl -u ${username}:${password} -X GET "http://${hostname}/service/rest/v1/components?repository=${repository}" | jq -r '.items[].id' | sort | uniq | xargs`
  if [ -z "$components" ];then
    break
  fi
  for t in $components;do
    t=$(echo $t | sed 's|\r||')
    curl -v -u ${username}:${password} -X DELETE "http://${hostname}/service/rest/v1/components/$t"
  done
done
