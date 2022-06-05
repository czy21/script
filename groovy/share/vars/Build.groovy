#!/usr/bin/env groovy
import org.ops.Util

def call() {
    pipeline {
        agent any
        environment {
            param_gradle_user_home = "/var/jenkins_home/tools/gradle"
            param_gradle_init_file = "${param_gradle_user_home}/init.gradle"
            param_yarn_cache = "/var/jenkins_home/tools/yarn/cache"
            param_project_root = org.ops.Util.ofPath(WORKSPACE,"${env.param_project_root}")
            param_project_name = "${env.param_project_name}"
            param_project_module = "${env.param_project_module}"
            param_git_repository_url = "${env.param_git_repository_url}"
            param_git_credential_id = "${env.param_git_credential_id}"
            param_global_env_file_id = "${env.param_global_env_file_id}"
            param_code_type = "${env.param_code_type}"
        }
        parameters {
            gitParameter branchFilter: 'origin/(.*)', name: 'param_branch', type: 'PT_BRANCH', defaultValue: 'master', useRepository: "${env.param_git_repository_url}"
        }
        stages {
            stage('clone') {
                steps {
                    script {
                        checkout([$class           : 'GitSCM',
                                  branches         : [
                                          [name: "${params.param_branch}"]
                                  ],
                                  extensions       : [
                                          [$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: true, recursiveSubmodules: true, reference: '', trackingSubmodules: false]
                                  ],
                                  userRemoteConfigs: [
                                          [credentialsId: "${env.param_git_credential_id}", url: "${env.param_git_repository_url}"]
                                  ]
                        ])
                    }
                }
            }
            stage('build') {
                steps {
                    script {
                        new org.ops.Docker().build()
                    }
                }
            }
        }
    }
}

