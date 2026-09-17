package org.ops

def deploy(Map inputs) {
    withCredentials([sshUserPrivateKey(credentialsId: 'opsor', keyFileVariable: 'SSH_PRIVATE_KEY')]) {
        withEnv(inputs.collect { k, v -> "${k}=${v}" }) {
            sh(script: libraryResource('org/ops/server-deploy.sh'))
        }
    }
}

return this