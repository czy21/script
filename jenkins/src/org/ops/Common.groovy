#!/usr/bin/env groovy
package org.ops

import org.ops.util.CollectionUtils
import org.ops.util.StringUtils

def writeParamToYaml() {
    Map<String, Object> param = readProperties text: sh(script: 'env | grep \'^param_\'', returnStdout: true).trim()
    param.each {
        if (it.getValue() in String && StringUtils.isNull(it.getValue() as String)) {
            param.put(it.getKey(), null)
        }
    }
    writeYaml file: '.jenkins/param.yaml', data: CollectionUtils.sortMapByKey(param), charset: 'UTF-8', overwrite: true
}

return this