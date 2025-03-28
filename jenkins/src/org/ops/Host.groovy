package org.ops


import org.ops.util.PathUtils
import org.ops.util.StringUtils

def deploy() {
    
    def deploy_file = ".jenkins/host-deploy.sh"
    def deploy_content = libraryResource "org/ops/host-deploy.sh"
    writeFile file: deploy_file, text: deploy_content, encoding: 'utf-8'

    withCredentials([sshUserPrivateKey(credentialsId: 'opsor', keyFileVariable: 'SSH_PRIVATE_KEY')]) {
        sh "chmod +x ${deploy_file};${deploy_file}"
    }
}

return this