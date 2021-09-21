def build(){
    env.HELM_REPO = env.HELM_REPO?: 'http://nexus.cluster2.com/repository/helm/'
    sh 'helm template ${RELEASE_NAME} ${HELM_JAVA_TEMPLATE_NAME} --version ${HELM_JAVA_TEMPLATE_VERSION} --namespace ${RELEASE_NAMESPACE} --set appVersion=${RELEASE_VERSION} --repo ${HELM_REPO}  2>&1 | tee deploy.yaml'
}


return this;