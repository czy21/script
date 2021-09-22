def build(){
    sh 'docker login ${REGISTRY_REPO} --username ${REGISTRY_USERNAME} --password ${REGISTRY_PASSWORD}'
    sh 'cd ${DOCKER_CONTEXT} && docker build --tag ${IMAGE_NAME}:${RELEASE_VERSION} --file Dockerfile . --no-cache --force-rm && cd'
    sh 'docker push ${IMAGE_NAME}:${RELEASE_VERSION}'
}

return this;