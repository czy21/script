#!/usr/bin/env groovy
package org.ops

import org.ops.util.CollectionUtils
import org.ops.util.StringUtils

def apply() {
    release = [
      java: {
        env.param_release_chart_name = env.param_helm_java_chart_name
        env.param_release_chart_version = env.param_helm_java_chart_version
      },
      go: {
        env.param_release_chart_name = env.param_helm_go_chart_name
        env.param_release_chart_version = env.param_helm_go_chart_version
      },
      py: {
        env.param_release_chart_name = env.param_helm_python_chart_name
        env.param_release_chart_version = env.param_helm_python_chart_version
      },
      web: {
        env.param_release_chart_name = env.param_helm_web_chart_name
        env.param_release_chart_version = env.param_helm_web_chart_version
      }
    ]
    release.get(env.param_code_type).call()

    def param = readProperties text: sh(script: 'env | grep \'^param_\'', returnStdout: true).trim()
    writeYaml file: '.jenkins/param.yaml', data: CollectionUtils.sortMapByKey(param), charset: 'UTF-8', overwrite: true
    withKubeConfig([credentialsId: env.param_kube_credential, serverUrl: env.param_kube_server]) {
        helm_cmd = StringUtils.format(
            "helm upgrade --install {0} {1} --version {2} --namespace {3} --repo {4} --values .jenkins/param.yaml --output yaml",
            env.param_release_name,
            env.param_release_chart_name,
            env.param_release_chart_version,
            env.param_release_namespace,
            env.param_helm_repo
        )
        sh "${helm_cmd}"
    }
}

return this;