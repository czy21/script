#!/bin/bash

project_root=${param_project_root}
code_type=${param_code_type}

if [ "${code_type}" == "dotnet" ];then
  (cd ${project_root};tar zcvf api.tar.gz -C build/ $(find build/ -type f \( ! -name "appsettings*.json" -o -name "appsettings.json" \) | sed 's|build/||'))
fi