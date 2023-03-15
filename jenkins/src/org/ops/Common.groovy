#!/usr/bin/env groovy
package org.ops

import org.ops.util.CollectionUtils
import org.ops.util.StringUtils

def writeParamToYaml() {
    Map<String, Object> param = readProperties text: sh(script: 'env | grep \'^param_\'', returnStdout: true).trim()
    param.each {
        it.value = StringUtils.isNotNull(it.getValue() as String) ? it.value : null
        return it
    }
    param = CollectionUtils.sortMapByKey(param)
    writeYaml file: '.jenkins/param.yaml', data: param, charset: 'UTF-8', overwrite: true
}

return this