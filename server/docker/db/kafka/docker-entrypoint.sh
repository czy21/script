#!/bin/bash

kafka_server_args=""
for t in $(env)
do
  if [[ $t =~ ^KAFKA_SERVER ]]; then
      opt=$(echo $t | sed 's/^KAFKA_SERVER_//')
      kafka_server_args+=" --override ${opt}"
  fi
done

if [[ -z $(env | grep '^KAFKA_SERVER_log.dirs') ]]; then
    kafka_server_args+=" --override log.dirs=/logs"
fi
echo -e "server args: ${kafka_server_args} \n"
echo -e "server starting... \n"
kafka-server-start.sh /opt/kafka/config/server.properties ${kafka_server_args}