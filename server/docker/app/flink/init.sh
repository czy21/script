#!/bin/bash

jar_dir={{ param_docker_data }}/{{ param_role_name }}/data/jar/
completed_job_dir={{ param_docker_data }}/{{ param_role_name }}/data/completed-jobs/
log_dir={{ param_docker_data }}/{{ param_role_name }}/log/
mkdir -p ${jar_dir} && chmod -R 777 ${jar_dir}
mkdir -p ${completed_job_dir} && chmod -R 777 ${completed_job_dir}
mkdir -p ${log_dir} && chmod -R 777 ${log_dir}