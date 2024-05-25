#!/usr/bin/env groovy
package org.ops.util

import java.nio.file.Path

static def ofPath(String first, String... more) {
    String[] moreParam = more.findAll { StringUtils.isNotEmpty(it) } as String[]
    return Path.of(first, moreParam).toString()
}

static def relativize(String p1, String p2) {
    return Path.of(p1).relativize(Path.of(p2)).toString()
}

return this