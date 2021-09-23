#!/usr/bin/env groovy
package org.ops

def build(){
    sh 'docker login ${PARAM_REGISTRY_REPO} --username ${PARAM_REGISTRY_USERNAME} --password ${PARAM_REGISTRY_PASSWORD}'
    sh 'docker build --tag ${PARAM_IMAGE_NAME}:${PARAM_RELEASE_VERSION} --file ${PARAM_DOCKER_FILE} ${PARAM_DOCKER_FILE_CONTEXT} --no-cache --force-rm'
    sh 'docker push ${PARAM_IMAGE_NAME}:${PARAM_RELEASE_VERSION}'
}

def prepare(){
    configFileProvider([configFile(fileId: "${PARAM_GLOBAL_ENV_FILE_ID}", targetLocation: 'env.groovy', variable: 'ENV_CONFIG')]) {
        load "env.groovy";
    }
    env.RELEASE_VERSION = params.BRANCH
    env.IMAGE_NAME="${PARAM_REGISTRY_REPO}/${PARAM_REGISTRY_DIR}/${PARAM_PROJECT_NAME}-${PARAM_PROJECT_MODULE}"
    env.DOCKER_FILE = "${PARAM_PROJECT_ROOT}/${PARAM_PROJECT_MODULE}/Dockerfile"
    env.DOCKER_FILE_CONTEXT = "${PARAM_PROJECT_ROOT}/${PARAM_PROJECT_MODULE}/"
}

return this