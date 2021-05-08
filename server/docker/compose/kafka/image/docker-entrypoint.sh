#!/usr/bin/env bash

KAFKA_CONF_FILE="${KAFKA_HOME}/config/server.properties"

set_config_option() {
  local key=$1
  local value=$2
  local conf_file=$3

  # escape periods for usage in regular expressions
  local escaped_key=$(echo ${key} | sed -e "s/\./\\\./g")

  echo "configuring => ${escaped_key} in ${conf_file}"

  # either override an existing entry, or append a new one
  if grep -E "^${escaped_key}=.*" "${conf_file}" > /dev/null; then
        sed -i -e "s/${escaped_key}=.*/${key}=${value}/g" "${conf_file}"
  else
        echo "${key}= ${value}" >> ${conf_file}
  fi
}

for VAR in $(env)
do
    env_var=$(echo "$VAR" | cut -d= -f1)

    # config server properties
    if [[ $env_var =~ ^KAFKA_SERVER ]]; then
        kafka_name=$(echo "$env_var" | cut -d_ -f3- | tr '[:upper:]' '[:lower:]' | tr _ .)
        set_config_option "$kafka_name" "${!env_var}" "${KAFKA_CONF_FILE}"
    fi

done

exec "$KAFKA_HOME/bin/kafka-server-start.sh" "$KAFKA_HOME/config/server.properties"