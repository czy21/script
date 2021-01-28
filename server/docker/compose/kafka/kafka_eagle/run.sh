#!/bin/bash
sh /usr/local/kafka_eagle/bin/ke.sh start
sleep 3
tail -f /usr/local/kafka_eagle/logs/log.log
