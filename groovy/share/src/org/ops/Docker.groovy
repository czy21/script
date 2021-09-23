#!/usr/bin/env groovy
package org.ops

def build(){
    sh 'docker login ${REGISTRY_REPO} --username ${REGISTRY_USERNAME} --password ${REGISTRY_PASSWORD}'
    sh 'docker build --tag ${IMAGE_NAME}:${RELEASE_VERSION} --file ${DOCKER_FILE} ${DOCKER_FILE_CONTEXT} --no-cache --force-rm'
    sh 'docker push ${IMAGE_NAME}:${RELEASE_VERSION}'
}

def prepare(){
    configFileProvider([configFile(fileId: "${GLOBAL_ENV_FILE_ID}", targetLocation: 'env.groovy', variable: 'ENV_CONFIG')]) {
        load "env.groovy";
    }
    env.RELEASE_VERSION = params.BRANCH
    env.IMAGE_NAME="${REGISTRY_REPO}/${REGISTRY_DIR}/${PROJECT_NAME}-${PROJECT_MODULE}"
    env.DOCKER_FILE = "${PROJECT_ROOT}/${PROJECT_MODULE}/Dockerfile"
    env.DOCKER_FILE_CONTEXT = "${PROJECT_ROOT}/${PROJECT_MODULE}/"
}

return this