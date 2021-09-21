def apply(){
    withKubeConfig([credentialsId: env.KUBE_CREDENTIAL, serverUrl: env.KUBE_SERVER]) {
        sh 'kubectl delete -f deploy.yaml --ignore-not-found=true && kubectl apply -f deploy.yaml'
    }
}

return this;