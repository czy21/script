#!/usr/bin/env groovy
package org.ops.util

import java.text.MessageFormat

static def isNull(String str) {
    return str == null || "null".equals(str)
}

static def isNotNull(String str) {
    return !isNull(str)
}

static def isEmpty(String str) {
    return isNull(str) || str.length() == 0
}

static def isNotEmpty(String str) {
    return !isEmpty(str)
}

static def join(String delimiter, String... items) {
    return items.findAll { isNotEmpty(it) }.join(delimiter)
}

static def format(String pattern, Object... arguments) {
    return MessageFormat.format(pattern, arguments)
}


return this