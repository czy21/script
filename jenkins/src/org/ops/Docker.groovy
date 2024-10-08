package org.ops

import org.ops.util.PathUtils
import org.ops.util.StringUtils

def build() {
    configFileProvider([configFile(fileId: "docker.config", targetLocation: '.jenkins/docker/config.json')]) {
        docker_config_dir = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/docker/")
        docker_image_tag = "${env.param_release_image}:${env.param_release_version}"
        docker_build_cmd = "docker build --tag ${docker_image_tag} --file ${env.param_docker_file} ${env.param_docker_context} --pull"
        if (StringUtils.isNotEmpty(env.param_docker_build_args)) {
            env.param_docker_build_args.split(",").each { t -> docker_build_cmd += " --build-arg $t" }
        }
        docker_push_cmd = "docker --config ${docker_config_dir} push ${docker_image_tag}"
        docker_rmi_cmd = "docker rmi ${docker_image_tag}"
        sh "${docker_build_cmd} && ${docker_push_cmd} && ${docker_rmi_cmd}"
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
    if (fileExists("${env.param_docker_compose_file}")) {
        sh "cp ${env.param_docker_compose_file} .jenkins/docker-compose.yaml"
    } else {
        deployMap.get(env.param_code_type).call()
    }
    withCredentials([dockerCert(credentialsId: 'docker-client', variable: 'DOCKER_CERT_PATH')]) {
        param_file = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/param.yaml")
        docker_compose_file = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/docker-compose.yaml")
        cmd = "DOCKER_TLS_VERIFY=1 DOCKER_HOST=tcp://${env.param_docker_deploy_host}:2376 docker-compose --project-name ${env.param_release_name} --file ${docker_compose_file} --env-file ${param_file} up --detach --remove-orphans"
        sh "${cmd}"
    }
}

return this
