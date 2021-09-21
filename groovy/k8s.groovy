def apply(){
    withKubeConfig([credentialsId: "${KUBE_CONFIG}", serverUrl: "${KUBE_SERVER}"]) {
        sh 'kubectl delete -f deploy.yaml --ignore-not-found=true && kubectl apply -f deploy.yaml'
    }
}

return this;