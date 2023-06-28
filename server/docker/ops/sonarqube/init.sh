#!/bin/bash

set -e
dirs=(data logs extensions)
for t in ${dirs[*]};do
  t_dir={{ param_docker_data }}/{{ param_role_name }}/$t/
  sudo mkdir -p ${t_dir} && sudo chown 1000:1000 ${t_dir}
done