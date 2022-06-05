#!/usr/bin/env groovy
package org.ops
import java.nio.file.Path

static def isEmpty(String str) {
    return str == null || str.length() == 0 || "null".equals(str)
}

static def isNotEmpty(String str) {
    println(Path.of("a","b/","c",""))
    return !isEmpty(str)
}

return this