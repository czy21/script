package org.ops


import org.ops.util.PathUtils
import org.ops.util.StringUtils

def build() {
    configFileProvider([configFile(fileId: "docker.config", targetLocation: '.jenkins/docker/config.json')]) {}

    def docker_file = env.param_docker_file

    if (!fileExists(docker_file)) {
        docker_file = ".jenkins/Dockerfile-${env.param_code_type}"
        def content = libraryResource "org/ops/Dockerfile-${env.param_code_type}"
        writeFile file: docker_file, text: content, encoding: 'utf-8'
    }

    def docker_config_dir = PathUtils.ofPath(env.WORKSPACE, ".jenkins/docker/")
    def docker_image_tag = "${env.param_release_image}:${env.param_release_version}"
    def sdk_version = env.getProperty("param_tool_${env.param_code_type}_version")
    def docker_build_cmd = "docker build --build-arg SDK_VERSION=${sdk_version} --tag ${docker_image_tag} --file ${docker_file} ${env.param_docker_context} --pull"
    if (StringUtils.isNotEmpty(env.param_docker_build_args)) {
        env.param_docker_build_args.split(",").each { t -> docker_build_cmd += " --build-arg $t" }
    }
    def docker_push_cmd = "docker --config ${docker_config_dir} push ${docker_image_tag}"
    def docker_rmi_cmd = "docker rmi ${docker_image_tag}"
    sh "${docker_build_cmd} && ${docker_push_cmd} && ${docker_rmi_cmd}"
}

def deploy() {

    def compose_file = env.param_docker_compose_file

    if (!fileExists(compose_file)) {
        compose_file = ".jenkins/docker-compose-${env.param_code_type}.yaml"
        def content = libraryResource "org/ops/docker-compose-${env.param_code_type}.yaml"
        writeFile file: compose_file, text: content, encoding: 'utf-8'
    }

    withCredentials([dockerCert(credentialsId: 'docker-client', variable: 'DOCKER_CERT_PATH')]) {
        def param_file = PathUtils.ofPath(env.WORKSPACE, ".jenkins/param.yaml")
        cmd = "DOCKER_TLS_VERIFY=1 DOCKER_HOST=tcp://${env.param_docker_deploy_host}:2376 docker-compose --project-name ${env.param_release_name} --file ${compose_file} --env-file ${param_file} up --detach --remove-orphans"
        sh "${cmd}"
    }
}

return this
