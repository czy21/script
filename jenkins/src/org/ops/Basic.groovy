#!/usr/bin/env groovy
package org.ops

import org.ops.util.CollectionUtils
import org.ops.util.StringUtils

def loadParam(Map inputs) {
    configFileProvider([configFile(fileId: "${inputs.param_global_env_file_id}", variable: 't')]) {
        def global_inputs = load(t)
        inputs.putAll(global_inputs.findAll { k, v -> !inputs.containsKey(k) })
    }
    inputs.each { k, v ->
        if (v instanceof Closure) {
            inputs[k] = v()
        }
    }
}

def writeParamToYaml(Map inputs) {
    writeYaml file: '.jenkins/inputs.yaml', data: CollectionUtils.sortMapByKey(inputs), charset: 'UTF-8', overwrite: true
}

return this