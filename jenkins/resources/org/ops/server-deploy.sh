#!/bin/bash

set -x

APP_DIR="${APP_DIR:-"/app"}"
SSH_HOST="${SSH_HOST:-opsor@${param_server_deploy_host}}"
SSH_ARGS="-o StrictHostKeyChecking=no"
NPM_RUN_SCRIPT="${NPM_RUN_SCRIPT:-"start"}"

[ -n "${param_release_name}" ] && return

if [ -n "${SSH_PRIVATE_KEY}" ];then
  SSH_ARGS+=" -i ${SSH_PRIVATE_KEY}"
fi

APP_CMD=

if [ "${param_code_type}" = "web" ];then
  APP_CMD+="rm -rf ${APP_DIR}/${param_release_name}/* && "
fi

APP_CMD+="mkdir -p ${APP_DIR}/${param_release_name}/ && tar -zxvf - -C ${APP_DIR}/${param_release_name}/ && chmod 777 ${APP_DIR}/${param_release_name}/"
TAR_SRC="${TAR_SRC:-.}"

if [ "${param_code_type}" = "java" ];then
  if [ "$TAR_SRC" = "." ]; then
    TAR_SRC="api.jar config"
  fi
fi

if [ "${param_code_type}" = "dotnet" ];then
  APP_CMD+="&& chmod +x ${APP_DIR}/${param_release_name}/api"
fi

if [ "${param_code_type}" = "nodejs" ];then
  APP_CMD+="&& npm --prefix ${APP_DIR}/${param_release_name}/ install"
fi

(cd ${param_project_root}/${param_project_module}/build && tar -zcf - ${TAR_SRC} --ignore-failed-read | ssh ${SSH_ARGS} ${SSH_HOST} "${APP_CMD}")

ssh ${SSH_ARGS} ${SSH_HOST} << SCRIPT
env_file=${APP_DIR}/${param_release_name}/.env
[ -f "\$env_file" ] || touch \$env_file

if [ "$param_code_type" = "java" ];then
    sudo tee /etc/systemd/system/${param_release_name}.service << EOF
[Unit]
Description=Java Application
After=network.target

[Service]
EnvironmentFile=\$env_file
WorkingDirectory=${APP_DIR}/${param_release_name}
ExecStart=${param_app_java_home}/bin/java ${param_app_args} -jar ${APP_DIR}/${param_release_name}/api.jar
Restart=always
User=\$USER

[Install]
WantedBy=multi-user.target

EOF
fi

if [ "$param_code_type" = "dotnet" ];then
    sudo tee /etc/systemd/system/${param_release_name}.service << EOF
[Unit]
Description=.NET Application
After=network.target

[Service]
EnvironmentFile=\$env_file
WorkingDirectory=${APP_DIR}/${param_release_name}
ExecStart=${APP_DIR}/${param_release_name}/api ${param_app_args}
Restart=always
User=\$USER

[Install]
WantedBy=multi-user.target

EOF
fi

if [ "$param_code_type" = "nodejs" ];then
    sudo tee /etc/systemd/system/${param_release_name}.service << EOF
[Unit]
Description=NodeJS Application
After=network.target

[Service]
EnvironmentFile=\$env_file
WorkingDirectory=${APP_DIR}/${param_release_name}
ExecStart=npm --prefix ${APP_DIR}/${param_release_name}/ run ${NPM_RUN_SCRIPT}
Restart=always
User=\$USER

[Install]
WantedBy=multi-user.target

EOF
fi

if [ -f "/etc/systemd/system/${param_release_name}.service" ];then
  sudo systemctl daemon-reload
  sudo systemctl restart ${param_release_name}
  sudo systemctl enable ${param_release_name}
fi
SCRIPT