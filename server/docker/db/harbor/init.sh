#!/bin/bash

sudo docker run --rm \
--entrypoint "" \
-v {{ param_docker_data }}/{{ param_role_name }}/conf/harbor.yml:/input/harbor.yml \
-v {{ param_docker_data }}/{{ param_role_name }}/data/:/data/ \
-v {{ param_docker_data }}/{{ param_role_name }}/data/:/compose_location/ \
-v {{ param_docker_data }}/{{ param_role_name }}/data/common/config/:/config/ \
--privileged \
goharbor/prepare:v2.5.3 sh -c "if [ ! -f /compose_location/docker-compose.yml ];then python3 main.py prepare;fi"