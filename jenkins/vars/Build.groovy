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
            booleanParam defaultValue: false, name: 'param_code_analysis'
        }
        stages {
            stage('clone') {
                steps {
                    script {
                        if (StringUtils.isEmpty("${env.param_git_branch}"){
                          env.param_git_branch = params.param_git_branch
                        }
                        checkout([$class           : 'GitSCM',
                                  branches         : [
                                          [name: "${env.param_git_branch}"]
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
            stage('param') {
                steps {
                    script {
                        def common = new Common()
                        common.loadParam()
                        env.param_project_context = PathUtils.ofPath(env.param_project_root, env.param_project_module)
                        env.param_docker_context = StringUtils.isNotNull(env.param_docker_context) ? PathUtils.ofPath(env.param_project_root, env.param_docker_context) : env.param_project_context
                        env.param_docker_file = PathUtils.ofPath(env.param_docker_context, "Dockerfile")
                        env.param_release_image = PathUtils.ofPath(env.param_registry_repo, env.param_registry_dir, env.param_release_name)
                        env.param_release_version = StringUtils.defaultIfEmpty(env.param_release_version, params.param_git_branch)
                        common.writeParamToYaml()
                    }
                }
            }
            stage('build') {
                steps {
                    script {
                        new Builder().build()
                    }
                }
            }
            stage('analysis') {
                when {
                    expression { params.param_code_analysis == true }
                }
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