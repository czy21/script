#!/bin/bash

set -e
sudo mkdir -p {{ param_docker_data }}/{{ param_role_name }}/data/
sudo cp -rv {{ param_docker_data }}/{{ param_role_name }}/conf/* {{ param_docker_data }}/{{ param_role_name }}/data/