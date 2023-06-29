#!/usr/bin/env groovy
package org.ops

import org.ops.util.PathUtils
import org.ops.util.StringUtils

def scan() {
    if (params.param_code_analysis) {
        env.SONARQUBE_HOME = "${tool 'sonarqube-4.8.0'}"
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
                        return StringUtils.format("{0} -Dsonar.java.binaries=**/build/classes", scanCmdPrefix,
                        )
                    }
            ]
            def scanCmd = scanCmdMap.get(env.param_code_type).call()
            sh "${scanCmd}"
        }
    }
}


return this