#!/bin/bash

set -e

docker build --tag ${param_registry_url}/${param_registry_dir}/confluence --file ${param_role_path}/Dockerfile-Confluence ${param_role_path}/ --no-cache --force-rm
docker build --tag ${param_registry_url}/${param_registry_dir}/jira --file ${param_role_path}/Dockerfile-Jira ${param_role_path}/ --no-cache --force-rm

docker push ${param_registry_url}/${param_registry_dir}/confluence
docker push ${param_registry_url}/${param_registry_dir}/jira