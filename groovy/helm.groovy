def build(){
    sh 'helm template ${RELEASE_NAME} ${RELEASE_TEMPLATE} --namespace ${RELEASE_NAMESPACE} --set appVersion="dev-bruce" --repo ${HELM_REPO} 2>&1 | tee deploy.yaml'
}



return this;