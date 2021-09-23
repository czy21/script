#!/usr/bin/env groovy

def call(Map map) {
    print map
    pipeline{
        agent any
        environment {
            PARAM_GRADLE_INIT_FILE = "/var/jenkins_home/tools/gradle/init.d/init.gradle"
            PARAM_PROJECT_ROOT    = "${WORKSPACE}/${map.PARAM_PROJECT_ROOT}"
            PARAM_PROJECT_NAME    = "${map.PARAM_PROJECT_NAME}"
            PARAM_PROJECT_MODULE  = "${map.PARAM_PROJECT_MODULE}"
            PARAM_GIT_REPOSITORY_URL = "${map.PARAM_GIT_REPOSITORY_URL}"
            PARAM_GIT_CREDENTIAL_ID  = "${map.PARAM_GIT_CREDENTIAL_ID}"
            PARAM_GLOBAL_ENV_FILE_ID = "${map.PARAM_GLOBAL_ENV_FILE_ID}"
            PARAM_NODEJS_HOME = "${tool 'node-v14.17.5'}"
            PARAM_PATH="${NODEJS_HOME}/bin:${PATH}"
        }
        parameters {
          gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH', type: 'PT_BRANCH',defaultValue: 'master',useRepository: "${map.PARAM_GIT_REPOSITORY_URL}"
        }
        stages {
            stage('clone'){
                steps{
                    script {
                        def g = new org.ops.Git()
                        g.checkout()
                    }
                }
            }
            stage('build'){
                when{
                    expression { BRANCH != 'master' }
                }
                steps{
                    script{
                        def d = new org.ops.Docker()
                        d.prepare()
                        sh 'nrm use taobao && yarn --cwd ${PARAM_PROJECT_ROOT}/${PARAM_PROJECT_MODULE} install && yarn --cwd ${PARAM_PROJECT_ROOT}/${PARAM_PROJECT_MODULE} --ignore-engines build'
                        d.build()
                    }
                }
            }
        }
    }
}

