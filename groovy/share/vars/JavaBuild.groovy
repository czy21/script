#!/usr/bin/env groovy

def call(Map map) {
    print map
    pipeline{
        agent any
        environment {
            GRADLE_INIT_FILE = "/var/jenkins_home/tools/gradle/init.d/init.gradle"
            PROJECT_ROOT    = "${WORKSPACE}/${map.PROJECT_ROOT}"
            PROJECT_NAME    = "${map.PROJECT_NAME}"
            PROJECT_MODULE  = "${map.PROJECT_MODULE}"
            GIT_REPOSITORY_URL = "${map.GIT_REPOSITORY_URL}"
            GIT_CREDENTIAL_ID  = "${map.GIT_CREDENTIAL_ID}"
            GLOBAL_ENV_FILE_ID = "${map.GLOBAL_ENV_FILE_ID}"
        }
        parameters {
          gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH', type: 'PT_BRANCH',defaultValue: 'master',useRepository: "${map.GIT_REPOSITORY_URL}"
        }
        stages {
            stage('clone'){
                steps{
                    script {
                        if (env.BRANCH == null){ env.BRANCH = 'master' }
                    }
                    checkout([$class: 'GitSCM', branches: [[name: "${BRANCH}"]],
                    extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: true, recursiveSubmodules: true, reference: '', trackingSubmodules: false]],
                    userRemoteConfigs: [[credentialsId: "${GIT_CREDENTIAL_ID}", url: "${GIT_REPOSITORY_URL}"]]
                    ])
                }
            }
            stage('build'){
                when{
                    expression { BRANCH != 'master' }
                }
                steps{
                    script{
                        configFileProvider([configFile(fileId: "${GLOBAL_ENV_FILE_ID}", targetLocation: 'env.groovy', variable: 'ENV_CONFIG')]) {
                            load "env.groovy";
                        }
                        env.RELEASE_VERSION = params.BRANCH
                        env.IMAGE_NAME="${REGISTRY_REPO}/${REGISTRY_DIR}/${PROJECT_NAME}-${PROJECT_MODULE}"
                        env.DOCKER_FILE = "${PROJECT_ROOT}/${PROJECT_MODULE}/Dockerfile"
                        env.DOCKER_FILE_CONTEXT = "${PROJECT_ROOT}/${PROJECT_MODULE}/"

                        sh 'chmod +x ${PROJECT_ROOT}/gradlew && ${PROJECT_ROOT}/gradlew --init-script ${GRADLE_INIT_FILE} --build-file ${PROJECT_ROOT}/build.gradle ${PROJECT_MODULE}:clean ${PROJECT_MODULE}:build -x test'
                        def d = new org.ops.Docker()
                        d.build()
                    }
                }
            }
        }
    }
}

