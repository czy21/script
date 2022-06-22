#!/usr/bin/env groovy
package org.ops

def apply() {

    // prepare
    configFileProvider([configFile(fileId: "${env.param_global_env_file_id}", targetLocation: '.jenkins-build/global.env')]) {
        load ".jenkins-build/global.env";
    }

    switch (env.param_code_type) {
        case "java":
            env.param_release_chart_name = env.param_helm_java_chart_name
            env.param_release_chart_version = env.param_helm_java_chart_version
            break;
        case "go":
            env.param_release_chart_name = env.param_helm_go_chart_name
            env.param_release_chart_version = env.param_helm_go_chart_version
            break;
        case "python":
            env.param_release_chart_name = env.param_helm_python_chart_name
            env.param_release_chart_version = env.param_helm_python_chart_version
            break;
        case "web":
            env.param_release_chart_name = env.param_helm_web_chart_name
            env.param_release_chart_version = env.param_helm_web_chart_version
            break;
        default:
            println(env.param_code_type + " not config" as String);
            return;
    }

    // k8s apply
    sh 'env | grep \'^param_\' | sed \'s/=/: /\' | sed \'s/^param_//\' > values.yaml'
    withKubeConfig([credentialsId: env.param_kube_credential, serverUrl: env.param_kube_server]) {
        helm_cmd = Util.format(
            "helm upgrade --install {0} {1} --version {2} --namespace {3} --repo {4} --values values.yaml --output yaml",
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