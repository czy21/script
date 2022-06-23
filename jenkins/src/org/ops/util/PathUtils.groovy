#!/usr/bin/env groovy
package org.ops.util

import java.nio.file.Path

static def ofPath(String first, String... more) {
    return Path.of(first, more.findAll { t -> StringUtils.isNotEmpty(t) } as String[]).toString()
}

return this