#!/bin/bash

set -e
data_dir={{ param_docker_data }}/{{ param_role_name }}/data/
sudo mkdir -p ${data_dir} && sudo chown 1000:1000 ${data_dir}