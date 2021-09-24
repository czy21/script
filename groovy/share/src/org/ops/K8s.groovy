#!/usr/bin/env groovy
package org.ops

def build(){
    sh 'env > env.conf'
    sh 'cat env.conf | grep \'^param_\' | paste -d "," -s | xargs helm template ${param_release_name} ${param_release_chart_name} --version ${param_release_chart_version} --namespace ${param_release_namespace} --repo ${param_helm_repo} --set-string  2>&1 | tee deploy.yaml'
}


def apply(){
    withKubeConfig([credentialsId: env.KUBE_CREDENTIAL, serverUrl: env.KUBE_SERVER]) {
        sh 'sleep 9999'
        // sh 'kubectl delete -f deploy.yaml --ignore-not-found=true && kubectl apply -f deploy.yaml'
    }
}

return this;