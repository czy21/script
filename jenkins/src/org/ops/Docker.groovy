package org.ops


import org.ops.util.PathUtils
import org.ops.util.StringUtils

def build(Map inputs) {
    configFileProvider([configFile(fileId: "docker.config", targetLocation: '.jenkins/docker/config.json')]) {}

    def docker_file = inputs.param_docker_file

    if (!fileExists(docker_file)) {
        docker_file = ".jenkins/Dockerfile-${inputs.param_code_type}"
        def content = libraryResource "org/ops/Dockerfile-${inputs.param_code_type}"
        writeFile file: docker_file, text: content, encoding: 'utf-8'
    }

    def docker_config_dir = PathUtils.ofPath(env.WORKSPACE, ".jenkins/docker/")
    def docker_image_tag = "${inputs.param_release_image}:${inputs.param_release_version}"
    def sdk_version = inputs.get("param_tool_"+inputs.param_code_type+"_version")
    def docker_build_cmd = "docker build --build-arg SDK_VERSION=${sdk_version} --tag ${docker_image_tag} --file ${docker_file} ${inputs.param_docker_context} --pull"
    if (StringUtils.isNotEmpty(inputs.param_docker_build_args)) {
        inputs.param_docker_build_args.split(",").each { t -> docker_build_cmd += " --build-arg $t" }
    }
    def docker_push_cmd = "docker --config ${docker_config_dir} push ${docker_image_tag}"
    def docker_rmi_cmd = "docker rmi ${docker_image_tag}"
    sh "${docker_build_cmd} && ${docker_push_cmd} && ${docker_rmi_cmd}"
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
        cmd = "DOCKER_TLS_VERIFY=1 DOCKER_HOST=tcp://${inputs.param_docker_deploy_host}:2376 docker-compose --project-name ${inputs.param_release_name} --file ${compose_file} --env-file ${param_file} up --detach --remove-orphans"
        sh "${cmd}"
    }
}

return this
