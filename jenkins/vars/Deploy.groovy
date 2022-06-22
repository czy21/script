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
                        new org.ops.K8s().apply()
                    }
                }
            }
        }
    }
}

