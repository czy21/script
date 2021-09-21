def build(){
    env.HELM_REPO = env.HELM_REPO?: 'http://nexus.cluster2.com/repository/helm/'
    sh 'helm template ${RELEASE_NAME} ${RELEASE_CHART_NAME} --version ${RELEASE_CHART_VERSION} --namespace ${RELEASE_NAMESPACE} --repo ${HELM_REPO} --set appVersion=${RELEASE_VERSION},envName=${ENV_NAME} 2>&1 | tee deploy.yaml'
}


return this;