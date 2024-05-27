package org.ops

import org.ops.util.PathUtils
import org.ops.util.StringUtils

def build() {
    configFileProvider([configFile(fileId: "docker.config", targetLocation: '.jenkins/docker/config.json')]) {
        env.DOCKER_HOME = "${tool 'docker'}"
        env.param_docker_cli = "${DOCKER_HOME}/bin/docker"
        docker_config_dir = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/docker/")
        docker_image_tag = "${env.param_release_image}:${env.param_release_version}"
        docker_build_cmd = "sudo ${param_docker_cli} build --tag ${docker_image_tag} --file ${env.param_docker_file} ${env.param_docker_context} --pull"
        if (StringUtils.isNotEmpty(env.param_docker_build_args)) {
            env.param_docker_build_args.split(",").each { t -> docker_build_cmd += " --build-arg $t" }
        }
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
    configFileProvider([
            configFile(fileId: 'docker-ssh-private-key', variable: 'DOCKER_SSH_PRIVATE_KEY')
    ]) {
        param_file = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/param.yaml")
        docker_compose_file = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/docker-compose.yaml")
        cmd="mkdir -p \$HOME/.ssh;echo 'Host *\n  StrictHostKeyChecking no' > \$HOME/.ssh/config;"
        cmd+="eval `ssh-agent`;chmod 600 ${DOCKER_SSH_PRIVATE_KEY};ssh-add ${DOCKER_SSH_PRIVATE_KEY};"
        cmd+="DOCKER_HOST=ssh://opsor@${env.param_docker_deploy_host} docker-compose --project-name ${env.param_release_name} --file ${docker_compose_file} --env-file ${param_file} up --detach --remove-orphans || error=true;"
        cmd+="ssh-agent -k;"
        cmd+="[ $error ] && exit -1"
        sh "${cmd}"
    }
}

return this
