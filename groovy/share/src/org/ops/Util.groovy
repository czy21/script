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
    for (int i = 0; i < more.length; i++) {
        if (isEmpty(more[i])) {
            more[i] = ""
        }
    }
    return Path.of(first, more).toString()
}

static def join(String delimiter, String... items) {
    return items.findAll { t -> isNotEmpty(t) }.join(delimiter)
}

return this