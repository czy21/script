#!/usr/bin/env groovy
package org.ops.util

import java.nio.file.Path

static def ofPath(String first, String... more) {
    return Path.of(first as String, more.findAll { StringUtils.isNotEmpty(it) } as String[]).toString()
}

static def relativize(String p1, String p2) {
    return Path.of(p1 as String).relativize(Path.of(p2 as String)).toString()
}

return this