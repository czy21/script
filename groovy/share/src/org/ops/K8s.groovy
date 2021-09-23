#!/usr/bin/env groovy
package org.ops

def build(){
    sh 'env > values.yaml'
    sh 'helm template ${RELEASE_NAME} ${RELEASE_CHART_NAME} --version ${RELEASE_CHART_VERSION} --namespace ${RELEASE_NAMESPACE} --repo ${HELM_REPO} --values values.yaml 2>&1 | tee deploy.yaml'
}


def apply(){
    withKubeConfig([credentialsId: env.KUBE_CREDENTIAL, serverUrl: env.KUBE_SERVER]) {
        sh 'sleep 9999'
        // sh 'kubectl delete -f deploy.yaml --ignore-not-found=true && kubectl apply -f deploy.yaml'
    }
}

return this;