#!/usr/bin/env groovy
import org.ops.Kubernetes
import org.ops.Common

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
                      image: 'registry.cluster.com/library/jenkins-inbound-agent'
                      securityContext:
                        runAsUser: 0
        '''
            }
        }
        stages {
            stage('deploy') {
                steps {
                    script {
                        new Common().loadEnv()
                        new Kubernetes().deploy()
                    }
                }
            }
        }
    }
}

