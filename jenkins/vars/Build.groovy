#!/usr/bin/env groovy

import org.ops.Builder
import org.ops.Basic
import org.ops.Docker
import org.ops.Server
import org.ops.util.PathUtils
import org.ops.util.StringUtils
import org.ops.util.ValidateUtils

def call() {
    pipeline {
        agent any
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

                        ValidateUtils.validateRequiredParams(env,["param_git_repository_url"])
                        
                        env.param_git_branch = StringUtils.defaultIfEmpty(env.param_git_branch, params.param_git_branch)

                        def gitExtensions = []
                        env.param_git_sparse_checkout = StringUtils.defaultIfEmpty(env.param_git_sparse_checkout, "").trim()
                        if (StringUtils.isNotEmpty(env.param_git_sparse_checkout)) {
                            def sparseCheckoutPaths = env.param_git_sparse_checkout.split(" ").collect { t -> [path: t] }
                            gitExtensions.add(sparseCheckout(sparseCheckoutPaths))
                        } else {
                            gitExtensions.add(submodule(parentCredentials: true, recursiveSubmodules: true, reference: ''))
                        }
                        checkout scmGit(
                                branches: [
                                        [name: env.param_git_branch]
                                ],
                                extensions: gitExtensions,
                                userRemoteConfigs: [
                                        [credentialsId: env.param_git_credential_id, url: env.param_git_repository_url]
                                ]
                        )
                    }
                }
            }
            stage('Param') {
                steps {
                    script {
                        ValidateUtils.validateRequiredParams(env,[
                                "param_global_env_file_id"
                        ])
                        def basic = new Basic()
                        basic.loadParam()

                        env.param_project_root = PathUtils.ofPath(env.WORKSPACE, env.param_project_root)
                        env.param_project_context = PathUtils.ofPath(env.param_project_root, env.param_project_module)

                        env.param_docker_build_enabled = StringUtils.defaultIfEmpty(env.param_docker_build_enabled, "true")
                        env.param_docker_context = StringUtils.isNotNull(env.param_docker_context) ? PathUtils.ofPath(env.param_project_root, env.param_docker_context) : env.param_project_context
                        env.param_docker_file = PathUtils.ofPath(env.param_docker_context, "Dockerfile")
                        env.param_docker_compose_file = PathUtils.ofPath(env.param_docker_context, "docker-compose.yaml")
                        env.param_release_image = PathUtils.ofPath(env.param_registry_repo, env.param_registry_dir, env.param_release_name)
                        env.param_release_version = StringUtils.defaultIfEmpty(env.param_release_version, params.param_git_branch)

                        env.param_sonarqube_server = StringUtils.defaultIfEmpty(env.param_sonarqube_server, "sonarqube")
                        env.param_sonarqube_project_key = StringUtils.defaultIfEmpty(env.param_sonarqube_project_key,env.param_release_name)
                        env.param_tool_java_version = StringUtils.defaultIfEmpty(env.param_tool_java_version,'jdk-21-graalvm')
                        env.param_tool_maven_version = StringUtils.defaultIfEmpty(env.param_tool_maven_version,'mvn-3.9')
                        env.param_tool_gradle_version = StringUtils.defaultIfEmpty(env.param_tool_gradle_version,'gradle-8.5')
                        env.param_tool_golang_version = StringUtils.defaultIfEmpty(env.param_tool_golang_version,'go-1.20')
                        env.param_tool_node_version = StringUtils.defaultIfEmpty(env.param_tool_node_version,'node-20.18')
                        env.param_tool_dotnet_version = StringUtils.defaultIfEmpty(env.param_tool_dotnet_version,'dotnet-9.0')

                        basic.writeParamToYaml()
                    }
                }
            }
            stage('Build') {
                steps {
                    script {
                        new Builder().exec()
                    }
                }
            }
            stage('Image') {
                when {
                    expression { env.param_docker_build_enabled == "true" }
                }
                steps {
                    script {
                        new Docker().build()
                    }
                }
            }
            stage('Deploy') {
                parallel {
                    stage('Server') {
                        when {
                            expression { StringUtils.isNotEmpty(env.param_server_deploy_host) }
                        }
                        steps {
                            script {
                                new Server().deploy()
                            }
                        }
                    }
                    stage('Docker') {
                        when {
                            expression { StringUtils.isNotEmpty(env.param_docker_deploy_host) }
                        }
                        steps {
                            script {
                                new Docker().deploy()
                            }
                        }
                    }
                }
            }
        }
    }
}