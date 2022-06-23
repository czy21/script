#!/usr/bin/env groovy
package org.ops.util

static def sortMapByKey(items) {
    return items.sort { t -> t.key }
}

return this