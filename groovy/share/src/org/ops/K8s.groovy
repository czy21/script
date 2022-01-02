#!/usr/bin/env groovy
package org.ops

def build(){
    sh 'env | grep \'^param_\' > env.conf'
    sh 'cat env.conf'
    sh 'cat env.conf | sed \'s/^param_//g\' | paste -d "," -s | xargs helm template ${param_release_name} ${param_release_chart_name} --version ${param_release_chart_version} --namespace ${param_release_namespace} --repo ${param_helm_repo} --set  2>&1 | tee deploy.yaml'
}


def apply(){
    withKubeConfig([credentialsId: env.param_kube_credential, serverUrl: env.param_kube_server]) {
        sh 'kubectl apply --filename=deploy.yaml'
    }
}


def prepare(Map map){
    configFileProvider([configFile(fileId: "${param_global_env_file_id}", targetLocation: 'global_env.groovy', variable: 'ENV_CONFIG')]) {
        load "global_env.groovy";
    }

    switch(env.param_code_type) {
     case "java":
        env.param_release_chart_name= env.param_helm_java_chart_name
        env.param_release_chart_version= env.param_helm_java_chart_version
        break;
     case "go":
        env.param_release_chart_name= env.param_helm_go_chart_name
        env.param_release_chart_version=env.param_helm_go_chart_version
        break;
     case "python":
        env.param_release_chart_name= env.param_helm_python_chart_name
        env.param_release_chart_version=env.param_helm_python_chart_version
        break;
     case "web":
        env.param_backend_url="${map.param_backend_url}"
        env.param_release_chart_name= env.param_helm_web_chart_name
        env.param_release_chart_version=env.param_helm_web_chart_version
        break;
     default:
        println [env.param_code_type,"not config"].join(" ");
        return;
    }
}

return this;