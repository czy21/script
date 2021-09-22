def build(){
    sh 'cd ${DOCKER_CONTEXT}'
    sh 'docker login ${REGISTRY_REPO} --username ${REGISTRY_USERNAME} --password ${REGISTRY_PASSWORD}'
    sh 'docker build --tag ${IMAGE_NAME}:${RELEASE_VERSION} --file Dockerfile . --no-cache --force-rm'
    sh 'docker push ${IMAGE_NAME}:${RELEASE_VERSION}'
    sh 'cd'
}

return this;