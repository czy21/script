#!/bin/bash

set -x

SSH_HOST="opsor@${param_deploy_host}"
SSH_ARGS="-o StrictHostKeyChecking=no -i ${SSH_PRIVATE_KEY}"

scp ${SSH_ARGS} .jenkins/host-start-api.sh ${SSH_HOST}:

if [ "${param_code_type}" == "dotnet" ];then
  (
    cd ${param_project_root}/build
    tar -zcf - . | ssh ${SSH_ARGS} ${SSH_HOST} "mkdir -p /app/${param_release_name}/ && tar -zxf - -C /app/${param_release_name}/ && ls -al /app/${param_release_name}/ && chmod +x /app/${param_release_name}/api"
  )
fi

ssh ${SSH_ARGS} ${SSH_HOST} << EOF
chmod +x host-start-api.sh
./host-start-api.sh -n ${param_release_name} -c ${param_code_type} -d /app/${param_release_name} -p "${param_app_args}"
EOF