#!/usr/bin/env groovy

def call(Map map) {
    pipeline{
        agent any
        environment {
            param_gradle_user_home = "/var/jenkins_home/tools/gradle"
            param_gradle_init_file = "${param_gradle_user_home}/init.gradle"
            param_project_root    = "${WORKSPACE}/${map.param_project_root}"
            param_project_name    = "${map.param_project_name}"
            param_project_module  = "${map.param_project_module}"
            param_git_repository_url = "${map.param_git_repository_url}"
            param_git_credential_id  = "${map.param_git_credential_id}"
            param_global_env_file_id = "${map.param_global_env_file_id}"
            param_code_type = "${map.param_code_type}"
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
                        map.each{ k, v -> env[k]=v }

//                         sh 'env'
                        println [env.param_project_name,env.param_project_module].findAll{it!=null}.join("-")

                        //def d = new org.ops.Docker()
                        //d.prepare(map)
                        //d.build()
                    }
                }
            }
        }
    }
}

