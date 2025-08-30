#!/usr/bin/env groovy
package org.ops

import org.ops.util.PathUtils
import org.ops.util.StringUtils

def scan() {
    env.SONARQUBE_HOME = tool 'sonarqube-7.2'
    env.PATH = "${SONARQUBE_HOME}/bin:${PATH}"
    def scanCmdPrefix = StringUtils.format(
            "sonar-scanner -Dsonar.projectKey={0} -Dsonar.projectVersion={1} -Dsonar.sources={2}",
            "${env.param_release_name}",
            "${env.param_release_version}",
            PathUtils.relativize("${env.WORKSPACE}", "${env.param_project_root}")
    )
    withSonarQubeEnv("${env.param_sonarqube_server}") {
        def scanCmdMap = [
                java: {
                    def cmd =  StringUtils.format("{0} -Dsonar.java.binaries=**/{1}/classes", scanCmdPrefix, "mvn" == env.param_java_build_tool ? "target" : "build")
                    sh "${cmd}"
                },
                web: {
                    def cmd = StringUtils.format("{0}", scanCmdPrefix)
                    sh "${cmd}"
                },
                dotnet: {
                    sh "dotnet new tool-manifest --force"
                    sh "dotnet tool install dotnet-sonarscanner"
                    sh "(cd ${env.param_project_root};dotnet tool run dotnet-sonarscanner begin /k:${env.param_release_name} /d:sonar.host.url=${SONAR_HOST_URL} /d:sonar.token=${SONAR_AUTH_TOKEN} /d:sonar.scanner.scanAll=false)"
                    configFileProvider([configFile(fileId: "nuget.config", variable: 'CONFIG_FILE_NUGET')]) {
                        sh "(cd ${env.param_project_root} && rm -rf bin build && dotnet publish --configfile ${CONFIG_FILE_NUGET} -c Release -r linux-x64 -p:PublishDir=build -p:DebugType=None -p:DebugSymbols=false)"
                    }
                    sh "(cd ${env.param_project_root};dotnet tool run dotnet-sonarscanner end /d:sonar.token=${SONAR_AUTH_TOKEN})"
                }
        ]
        scanCmdMap.get(env.param_code_type).call()
    }
}

return this