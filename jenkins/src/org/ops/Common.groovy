#!/usr/bin/env groovy
package org.ops

import org.ops.util.CollectionUtils

def writeParamToYaml() {
    def param = readProperties text: sh(script: 'env | grep \'^param_\'', returnStdout: true).trim()
    writeYaml file: '.jenkins/param.yaml', data: CollectionUtils.sortMapByKey(param as Map<String, Object>), charset: 'UTF-8', overwrite: true
}

return this