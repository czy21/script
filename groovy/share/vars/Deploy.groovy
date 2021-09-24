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
      environment {
        param_global_env_file_id = "${map.param_global_env_file_id}"
        param_env_name="${map.param_env_name}"
        param_code_type = "${map.param_code_type}"
        param_release_namespace="${map.param_release_namespace}"
        param_release_name="${map.param_release_name}"
        param_release_version="${map.param_release_version}"
      }
      stages{
        stage('deploy') {
          steps {
            script {
                def k = new org.ops.K8s()
                k.prepare(map)
                k.build()
                k.apply()
            }
          }
        }
      }
    }
}

