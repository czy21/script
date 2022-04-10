#!/usr/bin/env groovy
package org.ops

static def isEmpty(String str) {
    return str == null || str.length() == 0 || "null".equals(str)
}

static def isNotEmpty(String str) {
    return !isEmpty(str)
}

return this