#!/usr/bin/env groovy
package org.ops


import org.ops.util.PathUtils
import org.ops.util.StringUtils

def build() {
    env.param_project_context = PathUtils.ofPath(env.param_project_root, env.param_project_module)
    env.param_release_version = StringUtils.isNotEmpty(env.param_release_version)
                              ? env.param_release_version
                              : params.param_branch
    env.param_release_name = PathUtils.ofPath(
            env.param_registry_repo,
            env.param_registry_dir,
            StringUtils.isEmpty(env.param_release_name)
                    ? StringUtils.join("-", env.param_project_name, env.param_project_module)
                    : env.param_release_name
    )
    env.param_docker_context = StringUtils.isNull(env.param_docker_context)
                            ? env.param_project_context
                            : PathUtils.ofPath(env.param_project_root, env.param_docker_context)
    env.param_docker_file = PathUtils.ofPath(env.param_docker_context, "Dockerfile")

    def tool = [
            java: {
                env.JAVA_HOME = "${tool 'jdk-17'}"
                env.PATH = "${JAVA_HOME}/bin:${PATH}"
            },
            go  : {
                env.GO_HOME = "${tool 'go-v1.19.2'}"
                env.GOPROXY = env.param_go_proxy
                env.GOCACHE = env.param_go_cache
                env.GOSUMDB = "off"
                env.GOMODCACHE = env.param_go_mod_cache
                env.CGO_ENABLED = "0"
                env.PATH = "${GO_HOME}/bin:${PATH}"
            },
            web : {
                env.NODEJS_HOME = "${tool 'node-v16.14.0'}"
                env.PATH = "${NODEJS_HOME}/bin:${PATH}"
            }
    ]
    def cmd = [
            java : {
                tool.get("java").call()
                return StringUtils.format(
                        "chmod +x {0}/gradlew && {0}/gradlew --no-daemon --gradle-user-home {1} --init-script {2} --build-file {0}/build.gradle {3} -x test --refresh-dependencies",
                        env.param_project_root,
                        env.param_gradle_user_home,
                        env.param_gradle_init_file,
                        ["clean", "build"].collect { t -> StringUtils.join(":", env.param_project_module, t) }.join(" ")
                )
            },
            go   : {
                tool.get("go").call()
                return StringUtils.format(
                        "cd {0};go build -o build main.go;",
                        env.param_project_context
                )
            },
            web  : {
                tool.get("web").call()
                yarn_cmd = StringUtils.format(
                        "yarn --cwd {0} --registry {1} --cache-folder {2}",
                        env.param_project_context,
                        env.param_npm_repo,
                        env.param_yarn_cache
                )
                return StringUtils.format("{0} install --no-lockfile --update-checksums && {0} --ignore-engines build", yarn_cmd)
            },
            shell: {
                if (StringUtils.isNotEmpty(env.param_tools)) {
                    env.param_tools.split(",").each { tool.get(it).call() }
                }
                return StringUtils.format("chmod +x {0};{0}", PathUtils.ofPath(env.param_project_root, env.param_project_shell_file))
            }
    ]
    build_cmd = cmd.get(env.param_code_type).call()
    new Common().writeParamToYaml()
    sh "${build_cmd}"
    configFileProvider([configFile(fileId: "docker-config", targetLocation: '.jenkins/docker/config.json')]) {
        sh "docker build --tag ${env.param_release_name}:${env.param_release_version} --file ${env.param_docker_file} ${env.param_docker_context}"
        sh "docker --config .jenkins/docker/ push ${env.param_release_name}:${env.param_release_version}"
    }
}

return this