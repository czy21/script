#!/bin/bash

set -x

SSH_HOST="${SSH_HOST:-opsor@${param_deploy_host}}"
SSH_ARGS="-o StrictHostKeyChecking=no"

if [ -n "${SSH_PRIVATE_KEY}" ];then
  SSH_ARGS+=" -i ${SSH_PRIVATE_KEY}"
fi

if [ "${param_code_type}" == "dotnet" ];then
  (
    cd ${param_project_root}/build
    tar -zcf - . | ssh ${SSH_ARGS} ${SSH_HOST} "mkdir -p /app/${param_release_name}/ && tar -zxf - -C /app/${param_release_name}/ && ls -al /app/${param_release_name}/ && chmod +x /app/${param_release_name}/api"
  )
fi

if [ "${param_code_type}" == "midway" ];then
  (
    cd ${param_project_root}
    tar zcf - \
    --exclude='*.sh'  \
    --exclude='build' \
    --exclude='logs' \
    --exclude='node_modules' . | ssh ${SSH_ARGS} ${SSH_HOST} "mkdir -p /app/${param_release_name}/ && tar -zxf - -C /app/${param_release_name}/"
  )
fi

ssh ${SSH_ARGS} ${SSH_HOST} << SCRIPT
if [ "$param_code_type" == "dotnet" ];then
    sudo tee /etc/systemd/system/${param_release_name}.service << EOF
[Unit]
Description=.NET Application
After=network.target

[Service]
WorkingDirectory=/app/${param_release_name}
ExecStart=/app/${param_release_name}/api ${param_app_args}
Restart=always
User=opsor

[Install]
WantedBy=multi-user.target

EOF
fi

if [ "$param_code_type" == "midway" ];then
    sudo tee /etc/systemd/system/${param_release_name}.service << EOF
[Unit]
Description=.NET Application
After=network.target

[Service]
WorkingDirectory=/app/${param_release_name}
ExecStart=npm --prefix /app/${param_release_name}/ run start
Restart=always
User=opsor

[Install]
WantedBy=multi-user.target

EOF
fi

sudo systemctl daemon-reload
sudo systemctl restart ${param_release_name}
sudo systemctl enable ${param_release_name}
SCRIPT