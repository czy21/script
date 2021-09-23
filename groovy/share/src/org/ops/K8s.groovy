#!/usr/bin/env groovy
package org.ops

def build(){
    sh 'env > env.conf'
    sh 'cat env.conf | grep \'^PARAM_\' | paste -d "," -s | xargs helm template ${PARAM_RELEASE_NAME} ${PARAM_RELEASE_CHART_NAME} --version ${PARAM_RELEASE_CHART_VERSION} --namespace ${PARAM_RELEASE_NAMESPACE} --repo ${PARAM_HELM_REPO} --set-string  2>&1 | tee deploy.yaml'
}


def apply(){
    withKubeConfig([credentialsId: env.KUBE_CREDENTIAL, serverUrl: env.KUBE_SERVER]) {
        sh 'sleep 9999'
        // sh 'kubectl delete -f deploy.yaml --ignore-not-found=true && kubectl apply -f deploy.yaml'
    }
}

return this;