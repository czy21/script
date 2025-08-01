#!/bin/bash

set -x

APP_DIR="${APP_DIR:-"/app"}"
SSH_HOST="${SSH_HOST:-opsor@${param_deploy_host}}"
SSH_ARGS="-o StrictHostKeyChecking=no"
NPM_RUN_SCRIPT="${NPM_RUN_SCRIPT:-"start"}"

if [ -n "${SSH_PRIVATE_KEY}" ];then
  SSH_ARGS+=" -i ${SSH_PRIVATE_KEY}"
fi

APP_CMD="mkdir -p ${APP_DIR}/${param_release_name}/ && tar -zxvf - -C ${APP_DIR}/${param_release_name}/ && chmod 777 ${APP_DIR}/${param_release_name}/"

if [ "${param_code_type}" == "dotnet" ];then
  tar -zcf - -C ${param_project_root}/build . | ssh ${SSH_ARGS} ${SSH_HOST} "${APP_CMD} && chmod +x ${APP_DIR}/${param_release_name}/api"
fi

if [ "${param_code_type}" == "nodejs" ];then
  TAR_EXCLUDES="${TAR_EXCLUDES:-"build logs node_modules *.sh"}"
  TAR_EXCLUDES_ARGS=""
  for t in ${TAR_EXCLUDES};do
    TAR_EXCLUDES_ARGS+="--exclude=${t} "
  done
  (
    cd ${param_project_root}
    tar -zcf - ${TAR_EXCLUDES_ARGS} . | ssh ${SSH_ARGS} ${SSH_HOST} "${APP_CMD} && npm --prefix ${APP_DIR}/${param_release_name}/ install"
  )
fi

ssh ${SSH_ARGS} ${SSH_HOST} << SCRIPT
if [ "$param_code_type" == "dotnet" ];then
    sudo tee /etc/systemd/system/${param_release_name}.service << EOF
[Unit]
Description=.NET Application
After=network.target

[Service]
WorkingDirectory=${APP_DIR}/${param_release_name}
ExecStart=${APP_DIR}/${param_release_name}/api ${param_app_args}
Restart=always
User=\$USER

[Install]
WantedBy=multi-user.target

EOF
fi

if [ "$param_code_type" == "nodejs" ];then
    sudo tee /etc/systemd/system/${param_release_name}.service << EOF
[Unit]
Description=NodeJS Application
After=network.target

[Service]
WorkingDirectory=${APP_DIR}/${param_release_name}
ExecStart=npm --prefix ${APP_DIR}/${param_release_name}/ run ${NPM_RUN_SCRIPT}
Restart=always
User=\$USER

[Install]
WantedBy=multi-user.target

EOF
fi

sudo systemctl daemon-reload
sudo systemctl restart ${param_release_name}
sudo systemctl enable ${param_release_name}
SCRIPT