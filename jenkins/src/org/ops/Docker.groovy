package org.ops

import org.ops.util.PathUtils

def build() {
    configFileProvider([configFile(fileId: "docker.config", targetLocation: '.jenkins/docker/config.json')]) {
        env.DOCKER_HOME = "${tool 'docker'}"
        env.param_docker_cli = "${DOCKER_HOME}/bin/docker"
        docker_config_dir = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/docker/")
        docker_image_tag = "${env.param_release_image}:${env.param_release_version}"
        docker_build_cmd = "sudo ${param_docker_cli} build --tag ${docker_image_tag} --file ${env.param_docker_file} ${env.param_docker_context} --pull"
        docker_push_cmd = "sudo ${param_docker_cli} --config ${docker_config_dir} push ${docker_image_tag}"
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
    if (deployMap.containsKey(env.param_code_type)) {
        deployMap.get(env.param_code_type).call()
    }
    if (fileExists("${env.param_docker_compose_file}")) {
       sh "cp ${env.param_docker_compose_file} .jenkins/docker-compose.yaml"
    }
    docker_host = "tcp://${env.param_docker_deploy_host}:2375"
    param_file = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/param.yaml")
    docker_compose_file = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/docker-compose.yaml")
    docker_deploy_cmd = "DOCKER_HOST=${docker_host} sudo docker-compose --project-name ${env.param_release_name} --file ${docker_compose_file} --env-file ${param_file} up --detach --remove-orphans"
    sh "${docker_deploy_cmd}"
    sh "sudo ${env.param_docker_cli} image prune --force"
}

return this
