#!/bin/bash

server_args=""
for t in $(env)
do
  if [[ $t =~ ^KAFKA_SERVER ]]; then
      opt=$(echo $t | sed 's/^KAFKA_SERVER_//')
      server_args+=" --override ${opt}"
  fi
done

if [[ -z $(env | grep '^KAFKA_SERVER_log.dirs') ]]; then
    server_args+=" --override log.dirs=/logs"
fi
echo -e "server args: ${server_args} \nstarting... \n"
kafka-server-start.sh /opt/kafka/config/server.properties ${server_args}