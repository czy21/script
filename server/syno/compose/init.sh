#!/bin/bash

sudo curl -L "https://github.com/docker/compose/releases/download/v{{ param_docker_compose_version }}/docker-compose-$(uname -s)-$(uname -m)" -o /var/packages/ContainerManager/target/usr/bin/docker-compose