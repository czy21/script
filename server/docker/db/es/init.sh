#!/bin/bash
set -e

sudo sysctl -w vm.max_map_count=262144

data_dir={{ param_docker_data }}/{{ param_role_name }}/data/
sudo mkdir -p ${data_dir} && sudo chmod 777 -R ${data_dir}