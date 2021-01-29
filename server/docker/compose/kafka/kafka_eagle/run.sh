#!/bin/bash -e

echo "" > "$KE_HOME/conf/system-config.properties"

function updateConfig() {
    key=$1
    value=$2
    file=$3

    # Omit $value here, in case there is sensitive information
    echo "[Configuring] '$key' in '$file'"

    # If config exists in file, replace it. Otherwise, append to file.
    if grep -E -q "^#?$key=" "$file"; then
        sed -r -i "s@^#?$key=.*@$key=$value@g" "$file" #note that no config values may contain an '@' char
    else
        echo "$key=$value" >> "$file"
    fi
}

IFS=$'\n'
for VAR in $(env)
do
    env_var=$(echo "$VAR" | cut -d= -f1)
    if [[ $env_var =~ ^SYS_ ]]; then
        sys_name=$(echo "$env_var" | cut -d_ -f2- | tr '[:upper:]' '[:lower:]' | tr _ .)
        updateConfig "$sys_name" "${!env_var}" "$KE_HOME/conf/system-config.properties"
    fi

    if [[ $env_var =~ ^LOG4J_ ]]; then
        log4j_name=$(echo "$env_var" | tr '[:upper:]' '[:lower:]' | tr _ .)
        updateConfig "$log4j_name" "${!env_var}" "$KE_HOME/conf/log4j.properties"
    fi
done

$KE_HOME/bin/ke.sh start