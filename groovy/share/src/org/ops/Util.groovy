#!/usr/bin/env groovy
package org.ops
import java.nio.file.Path

static def isEmpty(String str) {
    return str == null || str.length() == 0 || "null".equals(str)
}

static def isNotEmpty(String str) {
    return !isEmpty(str)
}

static def ofPath(String first, String... more) {
    String[] items = more.findAll { t -> isNotEmpty(t) }
    return Path.of(first, items).toString()
}

static def join(String delimiter, String... items) {
    return items.findAll { t -> isNotEmpty(t) }.join(delimiter)
}

return this