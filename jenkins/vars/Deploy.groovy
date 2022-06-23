#!/usr/bin/env groovy

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
                      image: 'registry.cluster.com/library/jenkins-agent'
                      securityContext:
                        runAsUser: 0
        '''
            }
        }
        stages {
            stage('deploy') {
                steps {
                    script {
                        configFileProvider([configFile(fileId: "${env.param_global_env_file_id}", targetLocation: '.jenkins/default_param.groovy')]) {
                            param = load ".jenkins/default_param.groovy"
                            param.each{ k,v->
                              if (env.getProperty(k) == null) {
                                env.setProperty(k,v)
                              }
                            }
                        }
                        new org.ops.K8s().apply()
                    }
                }
            }
        }
    }
}

