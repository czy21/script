#!/usr/bin/env groovy
package org.ops

def build(){
    sh 'helm template ${RELEASE_NAME} ${RELEASE_CHART_NAME} --version ${RELEASE_CHART_VERSION} --namespace ${RELEASE_NAMESPACE} --repo ${HELM_REPO} --set appVersion=${RELEASE_VERSION},envName=${ENV_NAME} 2>&1 | tee deploy.yaml'
}


def apply(){
    withKubeConfig([credentialsId: env.KUBE_CREDENTIAL, serverUrl: env.KUBE_SERVER]) {
        sh 'kubectl delete -f deploy.yaml --ignore-not-found=true && kubectl apply -f deploy.yaml'
    }
}

return this;