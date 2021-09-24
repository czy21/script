#!/usr/bin/env groovy

def call(Map map) {
    pipeline{
      agent {
        kubernetes {
            cloud map.param_env_name
            yaml '''
              apiVersion: v1
              kind: Pod
              spec:
                volumes:
                - name: docker-sock
                  hostPath:
                    path: /var/run/docker.sock
                - name: docker-cmd
                  hostPath:
                    path: /usr/bin/docker
                - name: kubectl
                  hostPath:
                    path: /bin/kubectl
                containers:
                - name: jnlp
                  image: 'registry.cluster2.com/library/jenkins-agent'
                  securityContext:
                    runAsUser: 0
                  volumeMounts:
                  - name: docker-sock
                    mountPath: /var/run/docker.sock
                  - name: docker-cmd
                    mountPath: /usr/bin/docker
                  - name: kubectl
                    mountPath: /bin/kubectl
        '''
        }
      }
      stages{
        stage('deploy') {
          steps {
            script {
                def k = new org.ops.K8s()
                k.prepare()
                k.build()
                k.apply()
            }
          }
        }
      }
    }
}

