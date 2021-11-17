#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

docker build --tag ${param_registry_url}/${param_registry_dir}/confluence --file ${dir}/Dockerfile-Confluence ${dir}/ --no-cache --force-rm
docker build --tag ${param_registry_url}/${param_registry_dir}/jira --file ${dir}/Dockerfile-Jira ${dir}/ --no-cache --force-rm


docker push ${param_registry_url}/${param_registry_dir}/confluence
docker push ${param_registry_url}/${param_registry_dir}/jira