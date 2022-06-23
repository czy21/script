#!/usr/bin/env groovy
package org.ops.util

import com.cloudbees.groovy.cps.NonCPS

@NonCPS
static def sortMapByKey(Map<String, Object> map) {
    return map.sort { it.key }
}

return this