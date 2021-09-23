
def docker_build(){
    pipeline{
        agent any
//         environment {
//             GRADLE_INIT_FILE = "/var/jenkins_home/tools/gradle/init.d/init.gradle"
//             GLOBAL_ENV_FILE_ID = "dev.env"
//             GIT_REPOSITORY_CREDENTIAL_ID = "bruce"
//             GIT_REPOSITORY_URL = "git@gitee.com:czyhome/erp.git"
//             PROJECT_ROOT = "${WORKSPACE}/code/api"
//             PROJECT_NAME = "erp"
//             PROJECT_MODULE = "gateway"
//         }
//         parameters {
//           gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH', type: 'PT_BRANCH',defaultValue: 'master',useRepository: "${GIT_REPOSITORY_URL}"
//         }
        stages{
            stage('bbb'){
                steps{
                    sh 'echo hello'
                }
            }
        }
//         stages {
//             stage('clone'){
//                 steps{
//                     checkout([$class: 'GitSCM',
//                     branches: [[name: "${BRANCH}"]],
//                     extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: true, recursiveSubmodules: true, reference: '', trackingSubmodules: false]],
//                     userRemoteConfigs: [[credentialsId: "${GIT_REPOSITORY_CREDENTIAL_ID}", url: "${GIT_REPOSITORY_URL}"]]])
//                 }
//             }
//             stage('build'){
//                 when{
//                     expression { BRANCH != 'master' }
//                 }
//                 steps{
//                     script{
//                         configFileProvider([configFile(fileId: "${GLOBAL_ENV_FILE_ID}", targetLocation: 'env.groovy', variable: 'ENV_CONFIG')]) {
//                             load "env.groovy";
//                         }
//                         env.RELEASE_VERSION = params.BRANCH
//                         env.IMAGE_NAME = "${REGISTRY_REPO}/${REGISTRY_DIR}/${PROJECT_NAME}-${PROJECT_MODULE}"
//                         env.DOCKER_FILE = "${PROJECT_ROOT}/${PROJECT_MODULE}/Dockerfile"
//                         env.DOCKER_FILE_CONTEXT = "${PROJECT_ROOT}/${PROJECT_MODULE}/"
//
//                         sh 'docker login ${REGISTRY_REPO} --username ${REGISTRY_USERNAME} --password ${REGISTRY_PASSWORD}'
//                         sh 'docker build --tag ${IMAGE_NAME}:${RELEASE_VERSION} --file ${DOCKER_FILE} ${DOCKER_FILE_CONTEXT} --no-cache --force-rm'
//                         sh 'docker push ${IMAGE_NAME}:${RELEASE_VERSION}'
//                     }
//                 }
//             }
        // }
    }
}

return this