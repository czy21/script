#!/bin/bash
set -e

sudo sysctl -w vm.max_map_count=262144
data_dir={{ param_docker_data }}/{{ param_role_name }}/data/
for ((i=1;i<{{ param_db_minio_cluster_replicas }};i++));do
 data_node_dir=${data_dir}/${i}
 sudo mkdir -p ${data_node_dir} && sudo chmod 777 -R ${data_node_dir}
done