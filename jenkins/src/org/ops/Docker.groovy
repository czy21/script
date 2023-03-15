#!/usr/bin/env groovy
package org.ops


import org.ops.util.PathUtils
import org.ops.util.StringUtils

def build() {
    def common = new Common()
    env.param_project_context = PathUtils.ofPath(env.param_project_root, env.param_project_module)
    env.param_docker_context = StringUtils.isNotNull(env.param_docker_context) ? PathUtils.ofPath(env.param_project_root, env.param_docker_context) : env.param_project_context
    env.param_docker_file = PathUtils.ofPath(env.param_docker_context, "Dockerfile")
    env.param_release_name = PathUtils.ofPath(
            env.param_registry_repo,
            env.param_registry_dir,
            StringUtils.defaultIfEmpty(env.param_release_name, StringUtils.join("-", env.param_project_name, env.param_project_module))
    )
    env.param_release_version = StringUtils.defaultIfEmpty(env.param_release_version, params.param_branch)
    def sdkMap = [
            java  : {
                env.JAVA_HOME = "${tool 'jdk-17'}"
                env.PATH = "${JAVA_HOME}/bin:${PATH}"
            },
            go    : {
                env.GO_HOME = "${tool 'go-v1.20'}"
                env.GOPROXY = env.param_go_proxy
                env.GOSUMDB = "off"
                env.CGO_ENABLED = "0"
                env.PATH = "${GO_HOME}/bin:${PATH}"
            },
            web   : {
                env.NODEJS_HOME = "${tool 'node-v18.14.0'}"
                env.PATH = "${NODEJS_HOME}/bin:${PATH}"
            },
            dotnet: {
                env.DOTNET_HOME = "${tool 'net7.0-linux-64'}"
                env.DOTNET_SYSTEM_GLOBALIZATION_INVARIANT = 1
                env.PATH = "${DOTNET_HOME}:${PATH}"
            }
    ]
    def cmdMap = [
            java  : {
                sdkMap.get("java").call()
                return StringUtils.format(
                        "chmod +x {0}/gradlew && {0}/gradlew --init-script {2} --build-file {0}/build.gradle {3} -x test --refresh-dependencies",
                        env.param_project_root,
                        env.param_gradle_user_home,
                        PathUtils.ofPath("${env.WORKSPACE}", "${CONFIG_FILE_GRADLE}"),
                        ["clean", "build"].collect { t -> StringUtils.join(":", env.param_project_module, t) }.join(" ")
                )
            },
            go    : {
                sdkMap.get("go").call()
                return StringUtils.format("cd {0};go build -o build main.go;", env.param_project_context)
            },
            web   : {
                sdkMap.get("web").call()
                yarn_cmd = StringUtils.format("yarn --cwd {0} --registry {1}", env.param_project_context, env.param_npm_repo)
                return StringUtils.format("{0} install --no-lockfile --update-checksums && {0} --ignore-engines build", yarn_cmd)
            },
            dotnet: {
                sdkMap.get("dotnet").call()
                return StringUtils.format(
                        "rm -rf {0}/build && dotnet publish --configfile {1} -c Release -p:AssemblyName=api,PublishSingleFile=true --self-contained false {0} -o {0}/build",
                        env.param_project_root,
                        PathUtils.ofPath("${env.WORKSPACE}", "${CONFIG_FILE_NUGET}")
                )
            },
            shell : {
                if (StringUtils.isNotEmpty(env.param_tools)) {
                    env.param_tools.split(",").each { sdkMap.get(it).call() }
                }
                return StringUtils.format("chmod +x {0};{0}", PathUtils.ofPath(env.param_project_root, env.param_project_shell_file))
            }
    ]
    env.DOCKER_HOME = "${tool 'docker'}"
    configFileProvider([
            configFile(fileId: "init.gradle",  variable: 'CONFIG_FILE_GRADLE'),
            configFile(fileId: "nuget.config", variable: 'CONFIG_FILE_NUGET'),
            configFile(fileId: "docker-config", targetLocation: '.jenkins/docker/config.json')
    ]) {
        build_cmd = cmdMap.get(env.param_code_type).call()
        common.writeParamToYaml()
        docker_image_tag = "${env.param_release_name}:${env.param_release_version}"
        docker_config_dir = PathUtils.ofPath("${env.WORKSPACE}", ".jenkins/docker/")
        docker_build_cmd = "sudo ${DOCKER_HOME}/bin/docker build --tag ${docker_image_tag} --file ${env.param_docker_file} ${env.param_docker_context} --pull"
        docker_push_cmd = "sudo ${DOCKER_HOME}/bin/docker --config ${docker_config_dir} push ${docker_image_tag}"
        sh "${build_cmd} && ${docker_build_cmd} && ${docker_push_cmd}"
    }
}

return this