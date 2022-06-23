#!/usr/bin/env groovy
package org.ops.util

import java.nio.file.Path

static def ofPath(String first, String... more) {
    return Path.of(first, more.findAll { StringUtils.isNotEmpty(it) } as String[]).toString()
}

return this