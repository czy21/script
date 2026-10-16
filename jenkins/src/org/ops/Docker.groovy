package org.ops


import org.ops.util.PathUtils
import org.ops.util.StringUtils

def ssh_config(Map inputs, String target) {
    return """
    mkdir -p .jenkins/docker
    printf 'Host docker-remote\n\tHostName ${inputs.get('param_docker_' + target + '_host')}\n\tUser ${inputs.get('param_docker_' + target + '_user')}\n\tIdentityFile ${inputs.param_ssh_file}\n\tIdentitiesOnly yes\n\tStrictHostKeyChecking no\n\tUserKnownHostsFile /dev/null' > .jenkins/docker/ssh_config_${target}
    printf '#!/bin/bash\nexec /usr/bin/ssh -F $WORKSPACE/.jenkins/docker/ssh_config_${target} "\$@"' > .jenkins/docker/ssh
    chmod +x .jenkins/docker/ssh

    export PATH="$WORKSPACE/.jenkins/docker:$PATH"
    export DOCKER_HOST=ssh://docker-remote
    docker info
    """
}

def build(Map inputs) {

    def dockerConfigId = inputs.param_docker_config_env ? "${inputs.param_gradle_config_env}-docker.config" : 'docker.config'
    configFileProvider([configFile(fileId: dockerConfigId, targetLocation: '.jenkins/docker/config.json')]) {}
    env.DOCKER_CONFIG = PathUtils.ofPath(env.WORKSPACE, ".jenkins/docker/")

    def docker_file = inputs.param_docker_file
    if (!fileExists(docker_file)) {
        docker_file = ".jenkins/Dockerfile-${inputs.param_code_type}"
        def content = libraryResource "org/ops/Dockerfile-${inputs.param_code_type}"
        writeFile file: docker_file, text: content, encoding: 'utf-8'
    }

    def docker_image_tag = "${inputs.param_release_image}:${inputs.param_release_version}"

    sh """
    docker info
    docker build --pull --tag ${docker_image_tag} --build-arg BASE_IMAGE=${inputs.param_registry}/${inputs.param_registry_dir}/${inputs.get('param_tool_' + inputs.param_code_type + '_version')} ${inputs.param_docker_build_args ?: ''} --file ${docker_file} ${inputs.param_docker_context}
    docker push ${docker_image_tag}
    docker rmi ${docker_image_tag}
    """
    
}

def deploy(Map inputs) {

    def compose_file = inputs.param_docker_compose_file

    if (!fileExists(compose_file)) {
        compose_file = ".jenkins/docker-compose-${inputs.param_code_type}.yaml"
        def content = libraryResource "org/ops/docker-compose-${inputs.param_code_type}.yaml"
        writeFile file: compose_file, text: content, encoding: 'utf-8'
    }
    
    withCredentials([sshUserPrivateKey(credentialsId: 'opsor', keyFileVariable: 'SSH_FILE', usernameVariable: 'SSH_USER')]) {
        inputs.param_ssh_file = "${SSH_FILE}"
        inputs.param_ssh_user = "${SSH_USER}"
        inputs.param_docker_deploy_user = StringUtils.defaultIfEmpty(inputs.param_docker_deploy_user, inputs.param_ssh_user)

        sh """
        ${ssh_config(inputs, 'deploy')}
        docker compose --project-name ${inputs.param_release_name} --file ${compose_file} --env-file ${WORKSPACE}/.jenkins/inputs.yaml up --detach --remove-orphans
        """
    }
}

return this
