#!/usr/bin/env groovy
package org.ops

def checkout(){
    checkout([$class: 'GitSCM', branches: [[name: "${BRANCH}"]],
    extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: true, recursiveSubmodules: true, reference: '', trackingSubmodules: false]],
    userRemoteConfigs: [[credentialsId: "${GIT_CREDENTIAL_ID}", url: "${GIT_REPOSITORY_URL}"]]
    ])
}

return this