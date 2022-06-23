#!/usr/bin/env groovy
package org.ops


import org.ops.util.PathUtils
import org.ops.util.StringUtils

static def build(script) {
    script.env.param_project_context = PathUtils.ofPath(script.env.param_project_root, script.env.param_project_module)
    script.env.param_release_version = script.params.param_branch
    script.env.param_release_name = PathUtils.ofPath(
            script.env.param_registry_repo,
            script.env.param_registry_dir,
            StringUtils.isEmpty(script.env.param_release_name)
                    ? StringUtils.join("-", script.env.param_project_name, script.env.param_project_module)
                    : script.env.param_release_name
    )
    script.env.param_docker_context = script.env.param_docker_context == null
            ? script.env.param_project_context
            : PathUtils.ofPath(script.env.param_project_root, script.env.param_docker_context)
    script.env.param_docker_file = PathUtils.ofPath(script.env.param_docker_context, "Dockerfile")

    def tool = [
            java: {
                script.env.JAVA_HOME = "${script.tool 'jdk-17'}"
                script.env.PATH = "${script.env.JAVA_HOME}/bin:${script.PATH}"
            },
            go  : {
                script.env.GO_HOME = "${script.tool 'go-v1.18.2'}"
                script.env.GOPROXY = script.env.param_go_proxy
                script.env.GOCACHE = script.env.param_go_cache
                script.env.GOSUMDB = "off"
                script.env.GOMODCACHE = script.env.param_go_mod_cache
                script.env.CGO_ENABLED = "0"
                script.env.PATH = "${script.env.GO_HOME}/bin:${script.PATH}"
            },
            web : {
                script.env.NODEJS_HOME = "${script.tool 'node-v16.14.0'}"
                script.env.PATH = "${script.env.NODEJS_HOME}/bin:${script.PATH}"
            }
    ]
    def cmd = [
            java : {
                tool.get("java").call()
                return StringUtils.format(
                        "chmod +x {0}/gradlew && {0}/gradlew --gradle-user-home {1} --init-script {2} --build-file {0}/build.gradle {3} -x test --refresh-dependencies",
                        script.env.param_project_root,
                        script.env.param_gradle_user_home,
                        script.env.param_gradle_init_file,
                        ["clean", "build"].collect { t -> StringUtils.join(":", script.env.param_project_module, t) }.join(" ")
                )
            },
            go   : {
                tool.get("go").call()
                return StringUtils.format(
                        "cd {0};go build -o build main.go;",
                        script.env.param_project_context
                )
            },
            web  : {
                tool.get("web").call()
                def yarn_cmd = StringUtils.format(
                        "yarn --cwd {0} --registry {1} --cache-folder {2}",
                        script.env.param_project_context,
                        script.env.param_npm_repo,
                        script.env.param_yarn_cache
                )
                return StringUtils.format("{0} install --no-lockfile --update-checksums && {0} --ignore-engines build", yarn_cmd)
            },
            shell: {
                if (StringUtils.isNotEmpty(script.env.param_tools)) {
                    script.env.param_tools.split { "," }.each { t -> tool.get(t).call() }
                }
                return StringUtils.format("chmod +x {0};{0}", PathUtils.ofPath(script.env.param_project_root, script.env.param_project_shell_file))
            }
    ]
    def build_cmd = cmd.get(script.env.param_code_type).call()
    Common.writeParamToYaml(script)
    script.sh "${build_cmd}"
    script.sh "docker build --tag ${script.env.param_release_name}:${script.env.param_release_version} --file ${script.env.param_docker_file} ${script.env.param_docker_context}"
    script.configFileProvider([script.configFile(fileId: "docker-config", targetLocation: '.jenkins/docker/config.json')]) {
        script.sh "docker --config .jenkins/docker/ push ${script.env.param_release_name}:${script.env.param_release_version}"
    }
}

return this