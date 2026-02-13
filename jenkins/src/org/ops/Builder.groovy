#!/usr/bin/env groovy
package org.ops

import org.ops.util.PathUtils
import org.ops.util.StringUtils

def exec() {
    def pathMap = [
            java  : {
                env.JAVA_HOME = tool env.param_tool_java_version
                env.PATH = "${JAVA_HOME}/bin:${PATH}"
            },
            maven : {
                env.MAVEN_HOME = tool env.param_tool_maven_version
                env.PATH = "${MAVEN_HOME}/bin:${PATH}"
            },
            gradle: {
                env.GRADLE_HOME = tool env.param_tool_gradle_version
                env.PATH = "${GRADLE_HOME}/bin:${PATH}"
            },
            golang    : {
                env.GO_HOME = tool env.param_tool_golang_version
                env.GOPROXY = env.param_go_proxy
                env.GOSUMDB = "off"
                env.CGO_ENABLED = "0"
                env.PATH = "${GO_HOME}/bin:${PATH}"
            },
            node  : {
                env.NODEJS_HOME = tool env.param_tool_node_version
                env.PATH = "${NODEJS_HOME}/bin:${PATH}"
            },
            dotnet: {
                env.DOTNET_HOME = tool env.param_tool_dotnet_version
                env.DOTNET_SYSTEM_GLOBALIZATION_INVARIANT = 1
                env.PATH = "${DOTNET_HOME}:${PATH}"
            }
    ]

    if (StringUtils.isNotEmpty(env.param_tools)) {
        env.param_tools.split(",").each { pathMap.get(it).call() }
    }

    env.SONARQUBE_HOME = tool 'sonarqube-7.2'
    env.PATH = "${SONARQUBE_HOME}/bin:${PATH}"

    def sonarCmdPrefix = StringUtils.format(
            "sonar-scanner -Dsonar.projectKey=${env.param_sonarqube_project_key} -Dsonar.projectVersion=${env.param_release_version} -Dsonar.sources={0}",
            PathUtils.relativize(env.WORKSPACE, env.param_project_root)
    )

    def buildMap = [
            java  : {
                pathMap.get("java").call()
                if ("mvn" == env.param_java_build_tool || fileExists("${env.param_project_root}/pom.xml")) {
                    pathMap.get("maven").call()
                    configFileProvider([configFile(fileId: "mvn.config", variable: 'CONFIG_FILE')]) {
                        sh "mvn -B -s ${CONFIG_FILE} -f ${env.param_project_root}/pom.xml clean install -U -e -Dmaven.test.skip=true"
                        if (params.param_code_analysis == true) {
                            withSonarQubeEnv(env.param_sonarqube_server) {
                                sh "mvn -B -s ${CONFIG_FILE} -f ${env.param_project_root}/pom.xml org.sonarsource.scanner.maven:sonar-maven-plugin:sonar -Dsonar.projectKey=${env.param_sonarqube_project_key} -Dsonar.projectVersion=${env.param_release_version} -Dsonar.host.url=${SONAR_HOST_URL} -Dsonar.token=${SONAR_AUTH_TOKEN}"
                            }
                        }
                    }
                }
                else {
                    pathMap.get("gradle").call()
                    configFileProvider([configFile(fileId: "gradle.config", variable: 'CONFIG_FILE')]) {
                        sh "gradle --no-daemon -I ${CONFIG_FILE} -p ${env.param_project_root} clean build -U -x test"
                        if (params.param_code_analysis == true) {
                            withSonarQubeEnv(env.param_sonarqube_server) {
                                sh "gradle --no-daemon -I ${CONFIG_FILE} -p ${env.param_project_root} sonar -Dsonar.projectKey=${env.param_sonarqube_project_key} -Dsonar.projectName=${env.param_sonarqube_project_key} -Dsonar.projectVersion=${env.param_release_version} -Dsonar.host.url=${SONAR_HOST_URL} -Dsonar.token=${SONAR_AUTH_TOKEN}"
                            }
                        }
                    }
                }
            },
            go    : {
                pathMap.get("go").call()
                sh "cd ${env.param_project_context};go build -o build main.go;"
            },
            web   : {
                pathMap.get("node").call()
                sh "npm_config_registry=${env.param_npm_repo} npm_config_node_linker=hoisted pnpm --dir ${env.param_project_context} install && pnpm --dir ${env.param_project_context} run build"
                if (params.param_code_analysis == true) {
                    withSonarQubeEnv(env.param_sonarqube_server) {
                        def cmd = StringUtils.format("{0}", sonarCmdPrefix)
                        sh "${cmd}"
                    }
                }
            },
            dotnet: {
                pathMap.get("dotnet").call()
                configFileProvider([configFile(fileId: "nuget.config", variable: 'CONFIG_FILE_NUGET')]) {
                    if (params.param_code_analysis == true) {
                        withSonarQubeEnv(env.param_sonarqube_server) {
                            sh "dotnet new tool-manifest --force"
                            sh "dotnet tool install dotnet-sonarscanner --configfile ${CONFIG_FILE_NUGET}"
                            sh "(cd ${env.param_project_root};dotnet tool run dotnet-sonarscanner begin /k:${env.param_sonarqube_project_key} /v:${env.param_release_version} /d:sonar.host.url=${SONAR_HOST_URL} /d:sonar.token=${SONAR_AUTH_TOKEN} /d:sonar.scanner.scanAll=false)"
                        }
                    }
                    sh "(cd ${env.param_project_root} && rm -rf bin build && dotnet publish --configfile ${CONFIG_FILE_NUGET} -c Release -r linux-x64 -p:DebugType=None -p:DebugSymbols=false)"
                    if (params.param_code_analysis == true) {
                        withSonarQubeEnv(env.param_sonarqube_server) {
                            sh "(cd ${env.param_project_root};dotnet tool run dotnet-sonarscanner end /d:sonar.token=${SONAR_AUTH_TOKEN})"
                        }
                    }
                }
            },
            python: {
                sh "(cd ${env.param_project_root} && rm -rf build && mkdir -p build && find app -name '*.py' | xargs -I {} cp -rv --parents {} build/ && cp -rv main.py requirements.txt config/ build/)"
            },
            shell : {
                def cmd = StringUtils.format("chmod +x {0};{0}", PathUtils.ofPath(env.param_project_root, env.param_project_shell_file))
                sh "${cmd}"
            }
    ]
    if (buildMap.containsKey(env.param_code_type)) {
        buildMap.get(env.param_code_type).call()
    }
}

return this