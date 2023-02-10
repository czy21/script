#!/usr/bin/env groovy
package org.ops


import org.ops.util.PathUtils
import org.ops.util.StringUtils

def build() {
    env.param_project_context = PathUtils.ofPath(env.param_project_root, env.param_project_module)
    env.param_docker_context = StringUtils.isNotNull(env.param_docker_context) ? PathUtils.ofPath(env.param_project_root, env.param_docker_context) : env.param_project_context
    env.param_docker_file = PathUtils.ofPath(env.param_docker_context, "Dockerfile")
    env.param_release_name = PathUtils.ofPath(
            env.param_registry_repo,
            env.param_registry_dir,
            StringUtils.defaultIfEmpty(env.param_release_name, StringUtils.join("-", env.param_project_name, env.param_project_module))
    )
    env.param_release_version = StringUtils.defaultIfEmpty(env.param_release_version, params.param_branch)

    def toolMap = [
            java: {
                env.JAVA_HOME = "${tool 'jdk-17'}"
                env.PATH = "${JAVA_HOME}/bin:${PATH}"
            },
            go  : {
                env.GO_HOME = "${tool 'go-v1.20'}"
                env.GOPROXY = env.param_go_proxy
                env.GOSUMDB = "off"
                env.CGO_ENABLED = "0"
                env.PATH = "${GO_HOME}/bin:${PATH}"
            },
            web : {
                env.NODEJS_HOME = "${tool 'node-v18.14.0'}"
                env.PATH = "${NODEJS_HOME}/bin:${PATH}"
            }
    ]
    def cmdMap = [
            java : {
                toolMap.get("java").call()
                return StringUtils.format(
                        "chmod +x {0}/gradlew && {0}/gradlew --no-daemon --init-script {2} --build-file {0}/build.gradle {3} -x test --refresh-dependencies",
                        env.param_project_root,
                        env.param_gradle_user_home,
                        PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/init.gradle"),
                        ["clean", "build"].collect { t -> StringUtils.join(":", env.param_project_module, t) }.join(" ")
                )
            },
            go   : {
                toolMap.get("go").call()
                return StringUtils.format("cd {0};go build -o build main.go;", env.param_project_context)
            },
            web  : {
                toolMap.get("web").call()
                yarn_cmd = StringUtils.format("yarn --cwd {0} --registry {1}", env.param_project_context, env.param_npm_repo)
                return StringUtils.format("{0} install --no-lockfile --update-checksums && {0} --ignore-engines build", yarn_cmd)
            },
            shell: {
                if (StringUtils.isNotEmpty(env.param_tools)) {
                    env.param_tools.split(",").each { toolMap.get(it).call() }
                }
                return StringUtils.format("chmod +x {0};{0}", PathUtils.ofPath(env.param_project_root, env.param_project_shell_file))
            }
    ]
    build_cmd = cmdMap.get(env.param_code_type).call()
    new Common().writeParamToYaml()
    env.DOCKER_HOME = "${tool 'docker'}"
    configFileProvider([
            configFile(fileId: "init.gradle", targetLocation: '.jenkins/init.gradle'),
            configFile(fileId: "docker-config", targetLocation: '.jenkins/docker/config.json')
    ]) {
        docker_image_tag = "${env.param_release_name}:${env.param_release_version}"
        docker_config_dir = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/docker/")
        docker_build_cmd = "sudo ${DOCKER_HOME}/bin/docker build --tag ${docker_image_tag} --file ${env.param_docker_file} ${env.param_docker_context}"
        docker_push_cmd = "sudo ${DOCKER_HOME}/bin/docker --config ${docker_config_dir} push ${docker_image_tag}"
        sh "${build_cmd} && ${docker_build_cmd} && ${docker_push_cmd}"
    }
}

return this