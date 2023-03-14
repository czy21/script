#!/usr/bin/env groovy
package org.ops

import org.ops.util.CollectionUtils

def writeParamToYaml() {
    def param = readProperties text: sh(script: 'env | grep \'^param_\'', returnStdout: true).trim()
    writeYaml file: '.jenkins/param.yaml', data: CollectionUtils.sortMapByKey(param as Map<String, Object>), charset: 'UTF-8', overwrite: true
}

def getSDKMap() {
    def sdkMap = [
            java  : {
                env.JAVA_HOME = "${tool 'jdk-17'}"
                env.PATH = "${JAVA_HOME}/bin:${PATH}"
            },
            go    : {
                env.GO_HOME = "${tool 'go-v1.20'}"
                env.GOPROXY = env.param_go_proxy
                env.GOSUMDB = "off"
                env.CGO_ENABLED = "0"
                env.PATH = "${GO_HOME}/bin:${PATH}"
            },
            web   : {
                env.NODEJS_HOME = "${tool 'node-v18.14.0'}"
                env.PATH = "${NODEJS_HOME}/bin:${PATH}"
            },
            dotnet: {
                env.DOTNET_HOME = "${tool 'net7.0-linux-64'}"
                env.DOTNET_SYSTEM_GLOBALIZATION_INVARIANT = 1
                env.PATH = "${DOTNET_HOME}:${PATH}"
            }
    ]
    return sdkMap;
}

return this