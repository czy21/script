#!/usr/bin/env groovy
package org.ops.util

@NonCPS
static def sortMapByKey(Map<String, Object> map) {
    return map.sort { t -> t.key }
}

return this