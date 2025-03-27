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

SSH_HOST="opsor@${param_deploy_host}"
SSH_ARGS="-o StrictHostKeyChecking=no -i ${SSH_PRIVATE_KEY}"

scp ${SSH_ARGS} .jenkins/host-start-api.sh ${SSH_HOST}:

if [ -f "${archive_file}" ];then

  ssh ${SSH_ARGS} ${SSH_HOST} "mkdir -p /app/${param_release_name}/"
  scp ${SSH_ARGS} ${archive_file} ${SSH_HOST}:/app/${param_release_name}/

  if [ "${code_type}" == "dotnet" ];then
    ssh ${SSH_ARGS} -i ${SSH_PRIVATE_KEY} ${SSH_HOST} "cd /app/${param_release_name}/;tar -zxvf ${archive_name};chmod +x api;rm -fv ${archive_name}"
  fi

  ssh ${SSH_ARGS} ${SSH_HOST} "chmod +x host-start-api.sh && host-start-api.sh -n ${param_release_name} -c ${code_type} -d /app/${param_release_name}"

fi