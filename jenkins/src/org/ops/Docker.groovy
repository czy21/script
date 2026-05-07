package org.ops


import org.ops.util.PathUtils
import org.ops.util.StringUtils

def build(Map inputs) {

    def dockerConfigId = inputs.param_docker_config_env ? "${inputs.param_gradle_config_env}-docker.config" : 'docker.config'
    configFileProvider([configFile(fileId: dockerConfigId, targetLocation: '.jenkins/docker/config.json')]) {}
    env.DOCKER_CONFIG=PathUtils.ofPath(env.WORKSPACE, ".jenkins/docker/")

    def docker_file = inputs.param_docker_file

    if (!fileExists(docker_file)) {
        docker_file = ".jenkins/Dockerfile-${inputs.param_code_type}"
        def content = libraryResource "org/ops/Dockerfile-${inputs.param_code_type}"
        writeFile file: docker_file, text: content, encoding: 'utf-8'
    }

    def docker_image_tag = "${inputs.param_release_image}:${inputs.param_release_version}"
    def cmd = [
        "docker build",
        "--build-arg REGISTRY=${inputs.param_registry}",
        "--build-arg REGISTRY_DIR=${inputs.param_registry_dir}",
        "--build-arg SDK_VERSION=${inputs.get('param_tool_' + inputs.param_code_type + '_version')}",
    ]
    if (StringUtils.isNotEmpty(inputs.param_docker_build_args)) {
        cmd.add(inputs.param_docker_build_args)
    }
    cmd.add("--tag ${docker_image_tag} --file ${docker_file} ${inputs.param_docker_context} --pull")
    sh "${cmd.join(' ')} && docker push ${docker_image_tag} && docker rmi ${docker_image_tag}"
}

def deploy(Map inputs) {

    def compose_file = inputs.param_docker_compose_file

    if (!fileExists(compose_file)) {
        compose_file = ".jenkins/docker-compose-${inputs.param_code_type}.yaml"
        def content = libraryResource "org/ops/docker-compose-${inputs.param_code_type}.yaml"
        writeFile file: compose_file, text: content, encoding: 'utf-8'
    }

    withCredentials([dockerCert(credentialsId: 'docker-client', variable: 'DOCKER_CERT_PATH')]) {
        def param_file = PathUtils.ofPath(env.WORKSPACE, ".jenkins/inputs.yaml")
        def cmd = [
            "DOCKER_TLS_VERIFY=1 DOCKER_HOST=tcp://${inputs.param_docker_deploy_host}:2376",
            "docker-compose --project-name ${inputs.param_release_name} --file ${compose_file} --env-file ${param_file}",
            "up --detach --remove-orphans",
        ]
        sh "${cmd.join(' ')}"
    }
}

return this
