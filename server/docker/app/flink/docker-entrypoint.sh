#!/usr/bin/env bash

CONF_FILE="${FLINK_HOME}/conf/flink-conf.yaml"

if [ -n "${FLINK_PROPERTIES}" ]; then
    echo "${FLINK_PROPERTIES}" >> "${CONF_FILE}"
fi

exec "$@"