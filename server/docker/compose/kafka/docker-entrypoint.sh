#!/usr/bin/env bash

sh -c "exec kafka-server-start.sh /opt/kafka/config/server.properties $@"