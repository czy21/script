#!/bin/bash
set -e

sudo mkdir -p {{ param_docker_data }}/{{ param_role_name }}/{conf,data/cache}