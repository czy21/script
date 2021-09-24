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
    env.RELEASE_VERSION = params.BRANCH
    env.IMAGE_NAME="${param_registry_repo}/${param_registry_dir}/${param_project_name}-${param_project_module}"
    env.DOCKER_FILE = "${param_project_root}/${param_project_module}/Dockerfile"
    env.DOCKER_FILE_CONTEXT = "${param_project_root}/${param_project_module}/"
}

return this