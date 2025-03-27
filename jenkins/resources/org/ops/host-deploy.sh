#!/bin/bash

project_root=${param_project_root}
code_type=${param_code_type}

SSH_HOST="opsor@${param_deploy_host}"
SSH_ARGS="-o StrictHostKeyChecking=no -i ${SSH_PRIVATE_KEY}"

scp ${SSH_ARGS} .jenkins/host-start-api.sh ${SSH_HOST}:

if [ "${code_type}" == "dotnet" ];then
  (
    cd ${project_root}/build
    tar -zcf - . | ssh ${SSH_ARGS} ${SSH_HOST} "mkdir -p /app/${param_release_name}/ && tar -zxf - -C /app/${param_release_name}/ && ls -al /app/${param_release_name}/ && chmod +x /app/${param_release_name}/api"
  )
fi

ssh ${SSH_ARGS} ${SSH_HOST} "chmod +x host-start-api.sh && ./host-start-api.sh -n ${param_release_name} -c ${code_type} -d /app/${param_release_name}"