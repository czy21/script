#!/usr/bin/env groovy
package org.ops

import org.ops.util.StringUtils

def deploy(Map inputs) {
    def helm_chart_file = inputs.param_helm_chart_file

    if (fileExists(helm_chart_file)) {
        withKubeConfig([credentialsId: inputs.param_kube_credential]) {
            helm_cmd = StringUtils.format(
                    "helm dep up {0} && helm upgrade --install {1} {0} --version {2} --namespace {3} --values .jenkins/inputs.yaml --output yaml",
                    inputs.param_helm_chart_context,
                    inputs.param_release_name,
                    inputs.param_release_version,
                    inputs.param_release_namespace
            )
            sh "${helm_cmd}"
        }
        return
    }
    def chartMap = [
            java: {
                inputs.param_release_chart_name = inputs.param_helm_java_chart_name
                inputs.param_release_chart_version = inputs.param_helm_java_chart_version
            },
            dotnet: {
                inputs.param_release_chart_name = inputs.param_helm_dotnet_chart_name
                inputs.param_release_chart_version = inputs.param_helm_dotnet_chart_version
            },
            go  : {
                inputs.param_release_chart_name = inputs.param_helm_go_chart_name
                inputs.param_release_chart_version = inputs.param_helm_go_chart_version
            },
            py  : {
                inputs.param_release_chart_name = inputs.param_helm_python_chart_name
                inputs.param_release_chart_version = inputs.param_helm_python_chart_version
            },
            web : {
                inputs.param_release_chart_name = inputs.param_helm_web_chart_name
                inputs.param_release_chart_version = inputs.param_helm_web_chart_version
            }
    ]
    chartMap.get(inputs.param_code_type).call()
    withKubeConfig([credentialsId: inputs.param_kube_credential]) {
        helm_cmd = StringUtils.format(
                "helm upgrade --install {0} {1} --version {2} --namespace {3} --repo {4} --values .jenkins/inputs.yaml --output yaml",
                inputs.param_release_name,
                inputs.param_release_chart_name,
                inputs.param_release_chart_version,
                inputs.param_release_namespace,
                inputs.param_helm_repo
        )
        sh "${helm_cmd}"
    }
}

return this;