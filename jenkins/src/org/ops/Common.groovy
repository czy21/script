#!/usr/bin/env groovy
package org.ops

import org.ops.util.CollectionUtils
import org.ops.util.StringUtils

def loadParam() {
    configFileProvider([configFile(fileId: "${env.param_global_env_file_id}", variable: 'param')]) {
        param = load "${param}"
        param.each { k, v ->
            if (env.getProperty(k) == null) {
                env.setProperty(k, v)
            }
        }
    }
}

def writeParamToYaml() {
    Map<String, Object> param = readProperties text: sh(script: 'env | grep \'^param_\'', returnStdout: true).trim()
    param.each { k, v ->
        if (StringUtils.isNull(v as String)) {
            param.put(k, null)
        }
    }
    writeYaml file: '.jenkins/param.yaml', data: CollectionUtils.sortMapByKey(param), charset: 'UTF-8', overwrite: true
}

return this