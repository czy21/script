#!/usr/bin/env groovy
import org.ops.Docker
import org.ops.util.PathUtils

def call() {

    env.param_gradle_user_home = "/var/jenkins_home/tools/gradle"
    env.param_gradle_init_file = "/conf/init.gradle"
    env.param_go_mod_cache = "/var/jenkins_home/tools/go/pkg/mod"
    env.param_go_cache = "/var/jenkins_home/tools/go/cache/go-build"
    env.param_yarn_cache = "/var/jenkins_home/tools/yarn/cache"
    env.param_project_root = PathUtils.ofPath("${WORKSPACE}", "${env.param_project_root}")
    env.param_project_name = "${env.param_project_name}"
    env.param_project_module = "${env.param_project_module}"
    env.param_git_repository_url = "${env.param_git_repository_url}"
    env.param_git_credential_id = "${env.param_git_credential_id}"
    env.param_global_env_file_id = "${env.param_global_env_file_id}"
    env.param_code_type = "${env.param_code_type}"

    pipeline {
        agent any
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

