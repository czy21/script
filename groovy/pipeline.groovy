
def docker_build(Map map){
    print map
    pipeline{
        agent any
//         parameters {
//           gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH', type: 'PT_BRANCH',defaultValue: 'master'
//         }
        stages {
            stage('clone'){
                steps{
                    checkout([$class: 'GitSCM',branches: [[name: 'master']],extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: true, recursiveSubmodules: true, reference: '', trackingSubmodules: false]],userRemoteConfigs: [[credentialsId: map.GIT_REPOSITORY_CREDENTIAL_ID, url: map.GIT_REPOSITORY_URL]]])
                }
            }
//             stage('build'){
//                 when{
//                     expression { BRANCH != 'master' }
//                 }
//                 steps{
//                     script{
//                         configFileProvider([configFile(fileId: "${map.GLOBAL_ENV_FILE_ID}", targetLocation: 'env.groovy', variable: 'ENV_CONFIG')]) {
//                             load "env.groovy";
//                         }
//                         env.PROJECT_ROOT = "${WORKSPACE}/${map.PROJECT_ROOT}"
//                         env.PROJECT_NAME = "${map.PROJECT_NAME}"
//                         env.PROJECT_MODULE = "${map.PROJECT_MODULE}"
//
//                         env.RELEASE_VERSION = params.BRANCH
//                         env.IMAGE_NAME = "${REGISTRY_REPO}/${REGISTRY_DIR}/${PROJECT_NAME}-${PROJECT_MODULE}"
//                         env.DOCKER_FILE = "${PROJECT_ROOT}/${PROJECT_MODULE}/Dockerfile"
//                         env.DOCKER_FILE_CONTEXT = "${PROJECT_ROOT}/${PROJECT_MODULE}/"
//                         env.GRADLE_INIT_FILE = "/var/jenkins_home/tools/gradle/init.d/init.gradle"
//
//                         sh 'docker login ${REGISTRY_REPO} --username ${REGISTRY_USERNAME} --password ${REGISTRY_PASSWORD}'
//                         sh 'docker build --tag ${IMAGE_NAME}:${RELEASE_VERSION} --file ${DOCKER_FILE} ${DOCKER_FILE_CONTEXT} --no-cache --force-rm'
//                         sh 'docker push ${IMAGE_NAME}:${RELEASE_VERSION}'
//                     }
//                 }
//             }
        }
    }
}

return this