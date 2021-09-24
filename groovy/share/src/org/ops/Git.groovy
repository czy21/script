#!/usr/bin/env groovy
package org.ops

def checkout(){
    if (env.PARAM_BRANCH == null){ env.PARAM_BRANCH = 'master' }
    checkout([$class: 'GitSCM', branches: [[name: "${param_branch}"]],
            extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: true, recursiveSubmodules: true, reference: '', trackingSubmodules: false]],
            userRemoteConfigs: [[credentialsId: "${param_git_credential_id}", url: "${param_git_repository_url}"]]
    ])
}

return this