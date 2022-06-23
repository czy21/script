#!/usr/bin/env groovy
package org.ops.util

@NonCPS
static def sortMapByKey(items) {
    return items.sort { t -> t.key }
}

return this