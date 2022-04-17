#!/bin/bash

anonymous_dirs=(
{{ param_docker_data }}/{{ param_role_name }}/data/jar/
{{ param_docker_data }}/{{ param_role_name }}/data/completed-jobs/
{{ param_docker_data }}/{{ param_role_name }}/log/jmr/
{{ param_docker_data }}/{{ param_role_name }}/log/his/
)

for (( i=1;i<={{ param_bd_flink_cluster_tmr_replicas }};i++)); do
anonymous_dirs+=" {{ param_docker_data }}/{{ param_role_name }}/log/tmr/${i}"
done;

for t in ${anonymous_dirs[@]}; do
  sudo mkdir -p ${t} && sudo chmod -R 777 ${t}
done