def apply(){
    withKubeConfig([credentialsId: "${KUBE_CONFIG}", serverUrl: "${KUBE_SERVER}"]) {
        sh 'kubectl delete -f deploy.yaml --ignore-not-found=true && kubectl apply -f deploy.yaml'
    }
}

def deploy(){
    pipeline{
    agent {
        kubernetes {
            cloud 'dev'
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
        KUBE_CONFIG = 'kube-config-dev'
        KUBE_SERVER = 'https://192.168.2.21:6443'
        HELM_REPO   = 'http://nexus.cluster2.com/repository/helm/'
        RELEASE_TEMPLATE = 'java-template'
        RELEASE_NAMESPACE = 'erp'
        RELEASE_NAME = 'gateway'
        RELEASE_VERSION = 'dev-bruce'
    }
    stages{
        stage('deploy') {
        steps {
            sh 'helm template ${RELEASE_NAME} ${RELEASE_TEMPLATE} --namespace ${RELEASE_NAMESPACE} --set appVersion="${RELEASE_VERSION}" --repo ${HELM_REPO} 2>&1 | tee deploy.yaml'
            withKubeConfig([credentialsId: "${KUBE_CONFIG}", serverUrl: "${KUBE_SERVER}"]) {
            sh 'kubectl delete -f deploy.yaml --ignore-not-found=true && kubectl apply -f deploy.yaml'
            }
        }
        }
    }
    }
}

return this;