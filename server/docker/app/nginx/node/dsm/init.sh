#!/bin/bash
set -e

sudo mkdir -p {{ param_docker_data }}/{{ param_role_name }}/conf/cert/
sudo mkdir -p {{ param_docker_data }}/{{ param_role_name }}/data/log/