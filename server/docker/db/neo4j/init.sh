#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

sudo mkdir -p ${param_docker_data}/${param_role_name}/data/logs/