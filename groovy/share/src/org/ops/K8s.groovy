#!/usr/bin/env groovy
package org.ops

def build(){
    sh 'env > env.conf'
    sh 'cat env.conf | grep -v \'^param_\' | paste -d "," -s | xargs helm template ${param_release_name} ${param_release_chart_name} --version ${param_release_chart_version} --namespace ${param_release_namespace} --repo ${param_helm_repo} --set-string  2>&1 | tee deploy.yaml'
}


def apply(){
    withKubeConfig([credentialsId: env.KUBE_CREDENTIAL, serverUrl: env.KUBE_SERVER]) {
        sh 'sleep 9999'
        // sh 'kubectl delete -f deploy.yaml --ignore-not-found=true && kubectl apply -f deploy.yaml'
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
     case "web":
        env.param_backend_url="${map.param_backend_url}"
        env.param_release_chart_name= env.helm_web_chart_name
        env.param_release_chart_version=env.helm_web_chart_version
        break;
     default:
        println("The value is unknown");
        break;
    }
}

return this;