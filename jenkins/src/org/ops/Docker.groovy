package org.ops

import org.ops.util.PathUtils

def build() {
    configFileProvider([configFile(fileId: "docker.config", targetLocation: '.jenkins/docker/config.json')]) {
        env.DOCKER_HOME = "${tool 'docker'}"
        docker_cli = "${DOCKER_HOME}/bin/docker"
        docker_config_dir = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/docker/")
        docker_image_tag = "${env.param_release_name}:${env.param_release_version}"
        docker_build_cmd = "sudo ${docker_cli} build --tag ${docker_image_tag} --file ${env.param_docker_file} ${env.param_docker_context} --pull"
        docker_push_cmd = "sudo ${docker_cli} --config ${docker_config_dir} push ${docker_image_tag}"
        sh "${docker_build_cmd} && ${docker_push_cmd}"
    }
}

return this
