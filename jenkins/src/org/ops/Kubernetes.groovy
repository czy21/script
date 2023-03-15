#!/usr/bin/env groovy
package org.ops


import org.ops.util.StringUtils

def deploy() {
    def common = new Common()
    def chartMap = [
            java: {
                env.param_release_chart_name = env.param_helm_java_chart_name
                env.param_release_chart_version = env.param_helm_java_chart_version
            },
            go  : {
                env.param_release_chart_name = env.param_helm_go_chart_name
                env.param_release_chart_version = env.param_helm_go_chart_version
            },
            py  : {
                env.param_release_chart_name = env.param_helm_python_chart_name
                env.param_release_chart_version = env.param_helm_python_chart_version
            },
            web : {
                env.param_release_chart_name = env.param_helm_web_chart_name
                env.param_release_chart_version = env.param_helm_web_chart_version
            }
    ]
    chartMap.get(env.param_code_type).call()
    common.writeParamToYaml()
    withKubeConfig([credentialsId: env.param_kube_credential]) {
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