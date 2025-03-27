#!/bin/bash

project_root=${param_project_root}
code_type=${param_code_type}

archive_name="archive.tar.gz"
archive_file="${project_root}/${archive_name}"

if [ "${code_type}" == "dotnet" ];then
  (
    cd ${project_root}
    tar zcvf ${archive_name} -C build/ $(find build/ -type f \( ! -name "appsettings*.json" -o -name "appsettings.json" \) | sed 's|build/||')
  )
fi

SSH_ARGS="-o StrictHostKeyChecking=no -i ${SSH_PRIVATE_KEY}"
pwd
scp ${SSH_ARGS} .jenkins/host-start-api.sh opsor@${param_deploy_host}:

if [ -f "${archive_file}" ];then

  ssh ${SSH_ARGS} opsor@${param_deploy_host} "mkdir -p /app/${param_release_name}/"
  scp ${SSH_ARGS} ${archive_file} opsor@${param_deploy_host}:/app/${param_release_name}/

  if [ "${code_type}" == "dotnet" ];then
    ssh ${SSH_ARGS} -i ${SSH_PRIVATE_KEY} opsor@${param_deploy_host} "cd /app/${param_release_name}/;tar -zxvf ${archive_name};chmod +x api;rm -fv ${archive_name}"
  fi

  ssh ${SSH_ARGS} opsor@${param_deploy_host} "bash script/host-start-api.sh -n ${param_release_name} -c ${code_type} -d /app/${param_release_name}"

fi