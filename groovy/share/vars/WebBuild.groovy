#!/usr/bin/env groovy

def call(Map map) {
    print map
    pipeline{
        agent any
        environment {
            param_gradle_init_file = "/var/jenkins_home/tools/gradle/init.d/init.gradle"
            param_project_root    = "${WORKSPACE}/${map.param_project_root}"
            param_project_name    = "${map.param_project_name}"
            param_project_module  = "${map.param_project_module}"
            param_git_repository_url = "${map.param_git_repository_url}"
            param_git_credential_id  = "${map.param_git_credential_id}"
            param_global_env_file_id = "${map.param_global_env_file_id}"
            NODEJS_HOME = "${tool 'node-v14.17.5'}"
            PATH="${NODEJS_HOME}/bin:${PATH}"
        }
        parameters {
          gitParameter branchFilter: 'origin/(.*)', name: 'param_branch', type: 'PT_BRANCH',defaultValue: 'master',useRepository: "${map.param_git_repository_url}"
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
                    expression { param_branch != 'master' }
                }
                steps{
                    script{
                        def d = new org.ops.Docker()
                        d.prepare()
                        sh 'nrm use taobao && yarn --cwd ${param_project_root}/${param_project_module} install && yarn --cwd ${param_project_root}/${param_project_module} --ignore-engines build'
                        d.build()
                    }
                }
            }
        }
    }
}

