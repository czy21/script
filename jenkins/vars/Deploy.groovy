#!/usr/bin/env groovy

import org.ops.Builder
import org.ops.Basic
import org.ops.Kubernetes
import org.ops.Server
import org.ops.util.PathUtils
import org.ops.util.StringUtils
import org.ops.util.ValidateUtils

def call() {
    pipeline {
        agent {
            kubernetes {
                cloud env.param_env_name
                yaml '''
                  apiVersion: v1
                  kind: Pod
                  spec:
                    containers:
                      - name: jnlp
                        image: 'registry.czy21.com/library/jenkins-inbound-agent:3355.v388858a_47b_33-18-jdk21'
                        imagePullPolicy: Always
                        securityContext:
                          runAsUser: 0
        '''
            }
        }
        stages {
            stage('Clone') {
                when {
                    expression { StringUtils.isNotEmpty(env.param_git_repository_url) }
                }
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
                        env.param_helm_chart_context = StringUtils.isNotNull(env.param_helm_chart_context) ? PathUtils.ofPath(env.param_project_root, env.param_helm_chart_context) : env.param_project_context
                        env.param_helm_chart_file = PathUtils.ofPath(env.param_helm_chart_context, "Chart.yaml")

                        basic.writeParamToYaml()
                    }
                }
            }
            stage('Deploy') {
                steps {
                    script {
                        new Kubernetes().deploy()
                    }
                }
            }
        }
    }
}

