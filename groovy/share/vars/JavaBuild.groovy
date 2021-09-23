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
                        sh 'chmod +x ${PROJECT_ROOT}/gradlew && ${PROJECT_ROOT}/gradlew --init-script ${GRADLE_INIT_FILE} --build-file ${PROJECT_ROOT}/build.gradle ${PROJECT_MODULE}:clean ${PROJECT_MODULE}:build -x test'
                        d.build()
                    }
                }
            }
        }
    }
}

