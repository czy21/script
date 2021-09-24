#!/usr/bin/env groovy

def call(Map map) {
    print map

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
                configFileProvider([configFile(fileId: "${map.param_global_env_file_id}", targetLocation: 'env.groovy', variable: 'ENV_CONFIG')]) {
                    load "env.groovy";
                }
                env.param_env_name="${map.param_env_name}"
                env.param_release_namespace="${map.param_release_namespace}"
                env.param_release_name="${map.param_release_name}"
                env.param_release_version="${map.param_release_version}"
                switch(map.PARAM_TYPE) {
                 case "java":
                    env.param_release_chart_name= env.param_helm_java_chart_name
                    env.param_release_chart_version= env.param_helm_java_chart_version
                    break;
                 case "web":
                    env.param_backend_url="${map.param_backend_url}"
                    env.param_release_chart_name= env.helm_web_chart_name
                    env.param_release_chart_version=env.helm_web_chart_version
                    break;
                 default:
                    println("The value is unknown");
                    break;
                }
                def k = new org.ops.K8s()
                k.build()
                k.apply()
            }
          }
        }
      }
    }
}

