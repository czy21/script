#!/bin/bash

project_root=${param_project_root}
code_type=${param_code_type}

archive_name="archive.tar.gz"
archive_file="${project_root}/${archive_name}"

if [ "${code_type}" == "dotnet" ];then
  (
    cd ${project_root}
    rm -rf build/
    tar zcvf ${archive_name} -C build/ $(find build/ -type f \( ! -name "appsettings*.json" -o -name "appsettings.json" \) | sed 's|build/||')
  )
fi

if [ -f "${archive_file}" ];then
  echo "${archive_file}"
#   ssh opsor@${param_deploy_host} "mkdir -p /app/${param_release_name}/"
#   scp ${archive_file} opsor@${param_deploy_host}:/app/${param_release_name}/
#   ssh opsor@${param_deploy_host} "cd /app/${param_release_name}/;tar -zxvf ${archive_name};chmod +x api;rm -fv ${archive_name}"

#   ssh opsor@${param_deploy_host} "bash script/host-start-api.sh -n ${param_release_name} -c dotnet -d /app/${param_release_name}"

fi