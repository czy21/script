#!/bin/bash

set -e
conf_dir={{ param_docker_data }}/{{ param_role_name }}/conf/
data_dir={{ param_docker_data }}/{{ param_role_name }}/data/
sudo mkdir -p ${conf_dir} ${data_dir} && sudo chown 1000:1000 ${conf_dir} ${data_dir}