#!/usr/bin/env groovy
package org.ops

def build(){
    sh 'docker login ${param_registry_repo} --username ${param_registry_username} --password ${param_registry_password}'
    sh 'docker build --tag ${param_image_name}:${param_release_version} --file ${param_docker_file} ${param_docker_file_context} --no-cache --force-rm'
    sh 'docker push ${param_image_name}:${param_release_version}'
}

def prepare(){
    configFileProvider([configFile(fileId: "${param_global_env_file_id}", targetLocation: 'env.groovy', variable: 'ENV_CONFIG')]) {
        load "env.groovy";
    }
    env.param_release_version = params.param_branch
    env.param_image_name="${param_registry_repo}/${param_registry_dir}/${param_project_name}-${param_project_module}"
    env.param_docker_file = "${param_project_root}/${param_project_module}/Dockerfile"
    env.param_docker_file_context = "${param_project_root}/${param_project_module}/"
}

return this