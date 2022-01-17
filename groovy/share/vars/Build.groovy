#!/usr/bin/env groovy

def call() {
    pipeline{
        agent any
        environment {
            param_gradle_user_home   = "/var/jenkins_home/tools/gradle"
            param_gradle_init_file   = "${param_gradle_user_home}/init.gradle"
            param_yarn_cache          = "/var/jenkins_home/tools/yarn-cache"
            param_project_root       = "${WORKSPACE}/${env.param_project_root}"
            param_project_name       = "${env.param_project_name}"
            param_project_module     = "${env.param_project_module}"
            param_git_repository_url = "${env.param_git_repository_url}"
            param_git_credential_id  = "${env.param_git_credential_id}"
            param_global_env_file_id = "${env.param_global_env_file_id}"
            param_code_type          = "${env.param_code_type}"
        }
        parameters {
          gitParameter branchFilter: 'origin/(.*)', name: 'param_branch', type: 'PT_BRANCH',defaultValue: 'master',useRepository: "${env.param_git_repository_url}"
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
//                         d.build()
                    }
                }
            }
        }
    }
}

