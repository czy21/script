#!/usr/bin/env groovy

import org.ops.Builder
import org.ops.Basic
import org.ops.Docker
import org.ops.Server
import org.ops.util.PathUtils
import org.ops.util.StringUtils
import org.ops.util.ValidateUtils

def call(Map inputs) {
    pipeline {
        agent {
            label "${inputs.param_agent_label ?: ''}"
        }
        parameters {
            booleanParam defaultValue: false, name: 'param_code_analysis'
            booleanParam defaultValue: false, name: 'param_clean'
        }
        stages {
            stage('Clean') {
                when {
                    expression { params.param_clean == true }
                }
                steps {
                    cleanWs()
                }
            }
            stage('Clone') {
                steps {
                    script {

                        ValidateUtils.validateRequiredParams(inputs,["param_git_repository_url"])
                        
                        inputs.param_git_branch = StringUtils.defaultIfEmpty(inputs.param_git_branch, params.param_git_branch)

                        def gitExtensions = []
                        inputs.param_git_sparse_checkout = StringUtils.defaultIfEmpty(inputs.param_git_sparse_checkout, "").trim()
                        if (StringUtils.isNotEmpty(inputs.param_git_sparse_checkout)) {
                            def sparseCheckoutPaths = inputs.param_git_sparse_checkout.split(" ").collect { t -> [path: t] }
                            gitExtensions.add(sparseCheckout(sparseCheckoutPaths))
                        } else {
                            gitExtensions.add(submodule(parentCredentials: true, recursiveSubmodules: true, reference: ''))
                        }
                        dir('main') {
                            checkout scmGit(
                                    branches: [
                                            [name: inputs.param_git_branch]
                                    ],
                                    extensions: gitExtensions,
                                    userRemoteConfigs: [
                                            [url: inputs.param_git_repository_url, credentialsId: inputs.param_git_credential_id]
                                    ]
                            )
                        }
                        dir('script') {
                            checkout scmGit(
                                    branches: [
                                            [name: 'main']
                                    ],
                                    userRemoteConfigs: [
                                            [url: 'https://gitea.czy21.com:8443/czy21/script.git']
                                    ]
                            )
                        }
                    }
                }
            }
            stage('Param') {
                steps {
                    script {
                        ValidateUtils.validateRequiredParams(inputs,[
                                "param_global_env_file_id"
                        ])

                        def basic = new Basic()
                        basic.loadParam(inputs)

                        inputs.param_project_root = PathUtils.ofPath(env.WORKSPACE, 'main', inputs.param_project_root)

                        inputs.param_docker_context = PathUtils.ofPath(inputs.param_project_root, inputs.param_docker_context)
                        inputs.param_docker_file = PathUtils.ofPath(inputs.param_project_root, StringUtils.defaultIfEmpty(inputs.param_docker_file, 'Dockerfile'))
                        inputs.param_docker_compose_file = PathUtils.ofPath(inputs.param_project_root, StringUtils.defaultIfEmpty(inputs.param_docker_compose_file, 'docker-compose.yaml'))

                        inputs.param_release_image = StringUtils.defaultIfEmpty(inputs.param_release_image,PathUtils.ofPath(inputs.param_registry, inputs.param_registry_dir, inputs.param_release_name))
                        inputs.param_release_version = StringUtils.defaultIfEmpty(inputs.param_release_version, params.param_git_branch)

                        inputs.param_sonarqube_server = StringUtils.defaultIfEmpty(inputs.param_sonarqube_server, "sonarqube")
                        inputs.param_sonarqube_project_key = StringUtils.defaultIfEmpty(inputs.param_sonarqube_project_key,inputs.param_release_name)
                        inputs.param_tool_java_version = StringUtils.defaultIfEmpty(inputs.param_tool_java_version,'jdk-21-graalvm')
                        inputs.param_tool_maven_version = StringUtils.defaultIfEmpty(inputs.param_tool_maven_version,'mvn-3.9')
                        inputs.param_tool_gradle_version = StringUtils.defaultIfEmpty(inputs.param_tool_gradle_version,'gradle-9.7')
                        inputs.param_tool_nodejs_version = StringUtils.defaultIfEmpty(inputs.param_tool_nodejs_version,'nodejs-20.18')
                        inputs.param_tool_golang_version = StringUtils.defaultIfEmpty(inputs.param_tool_golang_version,'go-1.20')
                        inputs.param_tool_dotnet_version = StringUtils.defaultIfEmpty(inputs.param_tool_dotnet_version,'dotnet-9.0')

                        basic.writeParamToYaml(inputs)
                    }
                }
            }
            stage('Build') {
                steps {
                    script {
                        new Builder().exec(inputs)
                    }
                }
            }
            stage('Image') {
                when {
                    expression { inputs.param_docker_build_enabled }
                }
                steps {
                    script {
                        new Docker().build(inputs)
                    }
                }
            }
            stage('Deploy') {
                parallel {
                    stage('Server') {
                        when {
                            expression { StringUtils.isNotEmpty(inputs.param_server_deploy_host) }
                        }
                        steps {
                            script {
                                new Server().deploy(inputs)
                            }
                        }
                    }
                    stage('Docker') {
                        when {
                            expression { StringUtils.isNotEmpty(inputs.param_docker_deploy_host) }
                        }
                        steps {
                            script {
                                new Docker().deploy(inputs)
                            }
                        }
                    }
                }
            }
        }
    }
}