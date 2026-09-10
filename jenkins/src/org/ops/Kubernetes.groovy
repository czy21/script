#!/usr/bin/env groovy
package org.ops

import org.ops.util.StringUtils

def deploy(Map inputs) {
    def helm_chart_file = inputs.param_helm_chart_file

    if (fileExists(helm_chart_file)) {
        helm_cmd = "helm dep up ${inputs.param_helm_chart_context} && helm upgrade --install ${inputs.param_release_name} ${inputs.param_helm_chart_context} --version ${inputs.param_release_version} --namespace ${inputs.param_release_namespace} --values .jenkins/inputs.yaml --force --output yaml"
        sh "${helm_cmd}"
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
    
    helm_cmd = inputs.param_helm_repo.startsWith('oci://') 
                ? "helm upgrade --install ${inputs.param_release_name} ${inputs.param_release_chart_name} --version ${inputs.param_release_chart_version} --namespace ${inputs.param_release_namespace} --repo ${inputs.param_helm_repo} --values .jenkins/inputs.yaml --force --output yaml"
                : "helm upgrade --install ${inputs.param_release_name} ${inputs.param_helm_repo}/${inputs.param_release_chart_name} --version ${inputs.param_release_chart_version} --namespace ${inputs.param_release_namespace} --values .jenkins/inputs.yaml --force --output yaml"
    
    sh "${helm_cmd}"
}

return this;