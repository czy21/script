#!/usr/bin/env groovy
package org.ops

import org.ops.util.PathUtils
import org.ops.util.StringUtils

def build() {
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
                    env.PATH = "${MAVEN_HOME}/bin:${PATH}"
                    configFileProvider([configFile(fileId: "mvn.config", variable: 'CONFIG_FILE_MVN')]) {
                        cmd = StringUtils.format(
                                "mvn clean install -f {0}/pom.xml -s {1} -U -e -Dmaven.test.skip=true",
                                env.param_project_root,
                                "${CONFIG_FILE_MVN}")
                        sh "${cmd}"
                    }
                }
                else {
                    env.GRADLE_HOME = "${tool 'gradle-8.4'}"
                    env.PATH = "${GRADLE_HOME}/bin:${PATH}"
                    configFileProvider([configFile(fileId: "gradle.config", variable: 'CONFIG_FILE_GRADLE')]) {
                        base = StringUtils.format(
                                "gradle --init-script {1} --build-file {0}/build.gradle",
                                env.param_project_root,
                                "${CONFIG_FILE_GRADLE}"
                        )
                        cmd = StringUtils.format(
                                "{0} {1} -x test --refresh-dependencies",
                                base,
                                ["clean", "build"].collect { t -> StringUtils.join(":", env.param_project_module, t) }.join(" ")
                        )
                        sh "${cmd}"
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
    if (cmdMap.containsKey(env.param_code_type)) {
        cmdMap.get(env.param_code_type).call()
    }
}

return this