#!/usr/bin/env groovy
import org.ops.Docker
import org.ops.util.PathUtils

def call() {
    pipeline {
        agent any
        environment {
            param_project_root = PathUtils.ofPath("${env.WORKSPACE}", "${env.param_project_root}")
            param_project_name = "${env.param_project_name}"
            param_project_module = "${env.param_project_module}"
            param_git_repository_url = "${env.param_git_repository_url}"
            param_global_env_file_id = "${env.param_global_env_file_id}"
            param_code_type = "${env.param_code_type}"
        }
        parameters {
            credentials credentialType: 'com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey', defaultValue: 'opsor', name: 'param_git_ssh_private_id', required: false
            gitParameter branchFilter: 'origin/(.*)', name: 'param_git_branch', type: 'PT_BRANCH', defaultValue: 'master', useRepository: "${env.param_git_repository_url}"
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
                                          [credentialsId: "${params.param_git_ssh_private_id}", url: "${env.param_git_repository_url}"]
                                  ]
                        ])
                    }
                }
            }
            stage('build') {
                steps {
                    script {
                        configFileProvider([configFile(fileId: "${env.param_global_env_file_id}", variable: 'param')]) {
                            param = load "${param}"
                            param.each { k, v ->
                                if (env.getProperty(k) == null) {
                                    env.setProperty(k, v)
                                }
                            }
                        }
                        new Docker().build()
                    }
                }
            }
        }
    }
}

