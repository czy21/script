#!/bin/bash

data_dir={{ param_docker_data }}/{{ param_role_name }}/data/
sudo mkdir -p ${data_dir} && sudo chown -R 200 ${data_dir}