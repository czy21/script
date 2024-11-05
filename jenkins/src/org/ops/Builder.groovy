#!/usr/bin/env groovy
package org.ops

import org.ops.util.PathUtils
import org.ops.util.StringUtils

def build() {
    def pathMap = [
            java  : {
                env.JAVA_HOME = "${tool 'jdk-17'}"
                env.PATH = "${JAVA_HOME}/bin:${PATH}"
            },
            maven : {
                env.MAVEN_HOME = "${tool 'mvn-3.9'}"
                env.PATH = "${MAVEN_HOME}/bin:${PATH}"
            },
            gradle: {
                env.GRADLE_HOME = "${tool 'gradle-8.5'}"
                env.PATH = "${GRADLE_HOME}/bin:${PATH}"
            },
            go    : {
                env.GO_HOME = "${tool 'go-v1.20'}"
                env.GOPROXY = env.param_go_proxy
                env.GOSUMDB = "off"
                env.CGO_ENABLED = "0"
                env.PATH = "${GO_HOME}/bin:${PATH}"
            },
            node   : {
                env.NODEJS_HOME = "${tool 'node-v20.18.0'}"
                env.PATH = "${NODEJS_HOME}/bin:${PATH}"
            },
            dotnet: {
                env.DOTNET_HOME = "${tool 'net7.0-linux-64'}"
                env.DOTNET_SYSTEM_GLOBALIZATION_INVARIANT = 1
                env.PATH = "${DOTNET_HOME}:${PATH}"
            }
    ]
    if (StringUtils.isNotEmpty(env.param_tools)) {
        env.param_tools.split(",").each { pathMap.get(it).call() }
    }
    def buildMap = [
            java  : {
                pathMap.get("java").call()
                if ("mvn" == env.param_java_build_tool || fileExists("${env.param_project_context}/pom.xml")) {
                    pathMap.get("maven").call()
                    configFileProvider([configFile(fileId: "mvn.config", variable: 'CONFIG_FILE')]) {
                        sh "mvn -s ${CONFIG_FILE} -f ${env.param_project_context}/pom.xml clean install -U -e -Dmaven.test.skip=true"
                    }
                }
                if ("gradle" == env.param_java_build_tool || fileExists("${env.param_project_context}/build.gradle")) {
                    pathMap.get("gradle").call()
                    configFileProvider([configFile(fileId: "gradle.config", variable: 'CONFIG_FILE')]) {
                        sh "gradle --no-daemon -I ${CONFIG_FILE} -p ${env.param_project_context} clean build -U -x test"
                    }
                }
            },
            go    : {
                pathMap.get("go").call()
                cmd = StringUtils.format("cd {0};go build -o build main.go;", env.param_project_context)
                sh "${cmd}"
            },
            web   : {
                pathMap.get("node").call()
                cmd = StringUtils.format("{0} install --no-package-lock && {0} run build",StringUtils.format("npm --prefix {0} --registry {1}", env.param_project_context, env.param_npm_repo))
                sh "${cmd}"
            },
            yarn   : {
                pathMap.get("node").call()
                cmd = StringUtils.format("{0} install --no-lockfile --update-checksums && {0} --ignore-engines build",StringUtils.format("yarn --cwd {0} --registry {1}", env.param_project_context, env.param_npm_repo))
                sh "${cmd}"
            },
            dotnet: {
                pathMap.get("dotnet").call()
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
                cmd = StringUtils.format("chmod +x {0};{0}", PathUtils.ofPath(env.param_project_root, env.param_project_shell_file))
                sh "${cmd}"
            }
    ]
    if (buildMap.containsKey(env.param_code_type)) {
        buildMap.get(env.param_code_type).call()
    }
}

return this