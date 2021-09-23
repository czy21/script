#!/usr/bin/env groovy
package org.ops

def checkout(){
    if (env.BRANCH == null){ env.BRANCH = 'master' }
    checkout([$class: 'GitSCM', branches: [[name: "${PARAM_BRANCH}"]],
    extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: true, recursiveSubmodules: true, reference: '', trackingSubmodules: false]],
    userRemoteConfigs: [[credentialsId: "${PARAM_GIT_CREDENTIAL_ID}", url: "${PARAM_GIT_REPOSITORY_URL}"]]
    ])
}

return this