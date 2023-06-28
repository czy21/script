#!/usr/bin/env groovy
package org.ops


import org.ops.util.PathUtils
import org.ops.util.StringUtils

def build() {
    def common = new Common()
    env.param_project_context = PathUtils.ofPath(env.param_project_root, env.param_project_module)
    env.param_docker_context = StringUtils.isNotNull(env.param_docker_context) ? PathUtils.ofPath(env.param_project_root, env.param_docker_context) : env.param_project_context
    env.param_docker_file = PathUtils.ofPath(env.param_docker_context, "Dockerfile")
    env.param_release_image = PathUtils.ofPath(env.param_registry_repo,env.param_registry_dir,env.param_release_name)
    env.param_release_version = StringUtils.defaultIfEmpty(env.param_release_version, params.param_git_branch)
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
                if ("mvn" == env.param_java_build_tool) {
                    env.MAVEN_HOME = "${tool 'mvn-3.9'}"
                    configFileProvider([configFile(fileId: "mvn.config", variable: 'CONFIG_FILE_MVN')]) {
                        cmd = StringUtils.format(
                                "mvn clean install -f {0}/pom.xml -s {1} -U -e -Dmaven.test.skip=true",
                                env.param_project_root,
                                "${CONFIG_FILE_MVN}")
                        sh "${cmd}"
                    }
                }
                configFileProvider([configFile(fileId: "gradle.config", variable: 'CONFIG_FILE_GRADLE')]) {
                    cmd = StringUtils.format(
                            "chmod +x {0}/gradlew && {0}/gradlew --init-script {1} --build-file {0}/build.gradle {2} -x test --refresh-dependencies",
                            env.param_project_root,
                            "${CONFIG_FILE_GRADLE}",
                            ["clean", "build"].collect { t -> StringUtils.join(":", env.param_project_module, t) }.join(" ")
                    )
                    sh "${cmd}"
                    withSonarQubeEnv('sonarqube') {
                        snoarqube_cmd = StringUtils.format(
                                "chmod +x {0}/gradlew && {0}/gradlew --init-script {1} --build-file {0}/build.gradle {2}",
                                env.param_project_root,
                                "${CONFIG_FILE_GRADLE}",
                                "snoar -Dsonar.projectKey=czy21 -Dsonar.projectName='czy21'"
                        )
                        sh "${snoarqube_cmd}"
                    }
                }
            },
            go    : {
                sdkMap.get("go").call()
                cmd = StringUtils.format("cd {0};go build -o build main.go;", env.param_project_context)
                sh "${cmd}"
            },
            web   : {
                sdkMap.get("web").call()
                cmd = StringUtils.format("{0} install --no-lockfile --update-checksums && {0} --ignore-engines build",
                        StringUtils.format("yarn --cwd {0} --registry {1}", env.param_project_context, env.param_npm_repo)
                )
                sh "${cmd}"
            },
            dotnet: {
                sdkMap.get("dotnet").call()
                configFileProvider([configFile(fileId: "nuget.config", variable: 'CONFIG_FILE_NUGET')]) {
                    cmd = StringUtils.format(
                            "rm -rf {0}/build && dotnet publish --configfile {1} -c Release {0} -o {0}/build",
                            env.param_project_root,
                            "${CONFIG_FILE_NUGET}"
                    )
                    sh "${cmd}"
                }
            },
            shell : {
                if (StringUtils.isNotEmpty(env.param_tools)) {
                    env.param_tools.split(",").each { sdkMap.get(it).call() }
                }
                cmd = StringUtils.format("chmod +x {0};{0}", PathUtils.ofPath(env.param_project_root, env.param_project_shell_file))
                sh "${cmd}"
            }
    ]
    common.writeParamToYaml()
    cmdMap.get(env.param_code_type).call()
}

return this