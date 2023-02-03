#!/usr/bin/env groovy
import org.ops.Kubernetes

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
                        configFileProvider([configFile(fileId: "${env.param_global_env_file_id}", variable: 'param')]) {
                            param = load "${param}"
                            param.each { k, v ->
                                if (env.getProperty(k) == null) {
                                    env.setProperty(k, v)
                                }
                            }
                        }
                        new Kubernetes().deploy()
                    }
                }
            }
        }
    }
}

