package org.ops

import org.ops.util.PathUtils

def build() {
    configFileProvider([configFile(fileId: "docker.config", targetLocation: '.jenkins/docker/config.json')]) {
        env.DOCKER_HOME = "${tool 'docker'}"
        docker_cli = "${DOCKER_HOME}/bin/docker"
        docker_config_dir = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/docker/")
        docker_image_tag = "${env.param_release_image}:${env.param_release_version}"
        docker_build_cmd = "sudo ${docker_cli} build --tag ${docker_image_tag} --file ${env.param_docker_file} ${env.param_docker_context} --pull"
        docker_push_cmd = "sudo ${docker_cli} --config ${docker_config_dir} push ${docker_image_tag}"
        sh "${docker_build_cmd} && ${docker_push_cmd}"
    }
}

def deploy() {
    deployMap = [
            java: {
                configFileProvider([configFile(fileId: "docker-compose-java-v1.yaml", targetLocation: '.jenkins/docker-compose.yaml')]) {}
            },
            web : {
                configFileProvider([configFile(fileId: "docker-compose-web-v1.yaml", targetLocation: '.jenkins/docker-compose.yaml')]) {}
            }
    ]
    deployMap.get(env.param_code_type).call()
    param_file = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/param.yaml")
    docker_compose_file = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/docker-compose.yaml")
    docker_deploy_cmd = "sudo docker-compose --project-name ${env.param_release_name} --file ${docker_compose_file} --env-file ${param_file} up --detach"
    sh "${docker_deploy_cmd} && sudo ${env.param_docker_cli} image prune --force"
}

return this
