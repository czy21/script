#!/usr/bin/env groovy

def call(Map map) {
    print map

    pipeline{
      agent {
        kubernetes {
            cloud map.ENV_NAME
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
                configFileProvider([configFile(fileId: "${map.GLOBAL_ENV_FILE_ID}", targetLocation: 'env.groovy', variable: 'ENV_CONFIG')]) {
                    load "env.groovy";
                }
                env.ENV_NAME = "${map.ENV_NAME}"
                env.RELEASE_NAMESPACE = "${map.RELEASE_NAMESPACE}"
                env.RELEASE_NAME = "${map.RELEASE_NAME}"
                env.RELEASE_VERSION = "${map.RELEASE_VERSION}"
                switch(map.TYPE) {
                 case "java":
                    env.RELEASE_CHART_NAME    = env.HELM_JAVA_CHART_NAME
                    env.RELEASE_CHART_VERSION = env.HELM_JAVA_CHART_VERSION
                    break;
                 case "web":
                    env.RELEASE_CHART_NAME    = env.HELM_WEB_CHART_NAME
                    env.RELEASE_CHART_VERSION = env.HELM_WEB_CHART_VERSION
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

