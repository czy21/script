#!/usr/bin/env groovy
package org.ops

import org.ops.util.CollectionUtils

static def writeParamToYaml(script) {
    def param = script.readProperties text: script.sh(script: 'env | grep \'^param_\'', returnStdout: true).trim()
    script.writeYaml file: '.jenkins/param.yaml', data: CollectionUtils.sortMapByKey(param as Map<String, Object>), charset: 'UTF-8', overwrite: true
}

return this