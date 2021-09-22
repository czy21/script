def build(){
    sh 'docker login ${REGISTRY_URL} --username ${REGISTRY_USERNAME} --password ${REGISTRY_PASSWORD}'
    sh 'docker build --tag ${IMAGE_NAME}:${RELEASE_VERSION} --file ${DOCKER_FILE} ${DOCKER_CONTEXT} --no-cache --force-rm'
    sh 'docker push ${IMAGE_NAME}:${BRANCH}'
}

return this;