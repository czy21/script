#!/bin/bash

set -e

sudo cp -r {{ param_docker_data }}/{{ param_role_name }}/conf/ {{ param_docker_data }}/{{ param_role_name }}/data/