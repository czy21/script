package org.ops


import org.ops.util.PathUtils
import org.ops.util.StringUtils

def deploy() {
    withCredentials([sshUserPrivateKey(credentialsId: 'opsor', keyFileVariable: 'SSH_PRIVATE_KEY')]) {
        sh(script: libraryResource('org/ops/server-deploy.sh'))
    }
}

return this