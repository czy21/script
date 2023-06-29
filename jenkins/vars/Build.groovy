#!/usr/bin/env groovy
import org.ops.Analysis
import org.ops.Builder
import org.ops.Common
import org.ops.Docker
import org.ops.util.PathUtils
import org.ops.util.StringUtils

def call() {
    pipeline {
        agent any
        environment {
            param_project_root = PathUtils.ofPath("${env.WORKSPACE}", "${env.param_project_root}")
            param_project_module = "${env.param_project_module}"
            param_git_repository_url = "${env.param_git_repository_url}"
            param_git_credential_id = "${env.param_git_credential_id}"
            param_global_env_file_id = "${env.param_global_env_file_id}"
            param_code_type = "${env.param_code_type}"
            param_sonarqube_server = StringUtils.defaultIfEmpty("${env.param_sonarqube_server}", "sonarqube")
        }
        parameters {
            gitParameter branchFilter: 'origin/(.*)', name: 'param_git_branch', type: 'PT_BRANCH', defaultValue: 'master', useRepository: "${env.param_git_repository_url}"
            booleanParam defaultValue: false, name: 'param_code_analysis'
        }
        stages {
            stage('clone') {
                steps {
                    script {
                        checkout([$class           : 'GitSCM',
                                  branches         : [
                                          [name: "${params.param_git_branch}"]
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
                        new Common().loadParam()
                        new Builder().build()
                    }
                }
            }
            stage('analysis') {
                steps {
                    script {
                        new Analysis().scan()
                    }
                }
            }
            stage('dockerBuild') {
                steps {
                    script {
                        new Docker().build()
                    }
                }
            }
        }
    }
}

