#!/usr/bin/env groovy

def call(Map map) {
    pipeline{
        agent any
        environment {
            param_gradle_user_home   = "/var/jenkins_home/tools/gradle"
            param_gradle_init_file   = ["${param_gradle_user_home}","init.gradle"].join("/")
            param_project_root       = ["${WORKSPACE}","${map.param_project_root}"].join("/")

            param_project_name       = Optional.ofNullable(map.param_project_name).orElse("")
            param_project_module     = Optional.ofNullable(map.param_project_module).orElse("")
            param_git_repository_url = Optional.ofNullable(map.param_git_repository_url).orElse("")
            param_git_credential_id  = Optional.ofNullable(map.param_git_credential_id).orElse("")
            param_global_env_file_id = Optional.ofNullable(map.param_global_env_file_id).orElse("")
            param_code_type          = Optional.ofNullable(map.param_code_type).orElse("")
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
                        sh 'env'
                        println env.param_project_module
                        //d.prepare(map)
                        //d.build()
                    }
                }
            }
        }
    }
}

