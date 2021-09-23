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
            NODEJS_HOME = "${tool 'node-v14.17.5'}"
            PATH="${NODEJS_HOME}/bin:${PATH}"
        }
        parameters {
          gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH', type: 'PT_BRANCH',defaultValue: 'master',useRepository: "${map.GIT_REPOSITORY_URL}"
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
                        sh 'nrm use taobao && yarn --cwd ${PROJECT_ROOT}/${PROJECT_MODULE} install && yarn --cwd ${PROJECT_ROOT}/${PROJECT_MODULE} --ignore-engines build'
                        d.build()
                    }
                }
            }
        }
    }
}

