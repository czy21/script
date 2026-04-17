#!/usr/bin/env groovy

import org.ops.Builder
import org.ops.Basic
import org.ops.Kubernetes
import org.ops.Server
import org.ops.util.PathUtils
import org.ops.util.StringUtils
import org.ops.util.ValidateUtils

def call(Map inputs) {
    pipeline {
        agent {
            kubernetes {
                cloud inputs.param_env_name
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
                    expression { StringUtils.isNotEmpty(inputs.param_git_repository_url) }
                }
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
                        checkout scmGit(
                                branches: [
                                        [name: inputs.param_git_branch]
                                ],
                                extensions: gitExtensions,
                                userRemoteConfigs: [
                                        [credentialsId: inputs.param_git_credential_id, url: inputs.param_git_repository_url]
                                ]
                        )
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

                        inputs.param_project_root = PathUtils.ofPath(env.WORKSPACE, inputs.param_project_root)
                        inputs.param_project_context = PathUtils.ofPath(inputs.param_project_root, inputs.param_project_module)
                        inputs.param_helm_chart_context = StringUtils.isNotNull(inputs.param_helm_chart_context) ? PathUtils.ofPath(inputs.param_project_root, inputs.param_helm_chart_context) : inputs.param_project_context
                        inputs.param_helm_chart_file = PathUtils.ofPath(inputs.param_helm_chart_context, "Chart.yaml")

                        basic.writeParamToYaml(inputs)
                    }
                }
            }
            stage('Deploy') {
                steps {
                    script {
                        new Kubernetes().deploy(inputs)
                    }
                }
            }
        }
    }
}

