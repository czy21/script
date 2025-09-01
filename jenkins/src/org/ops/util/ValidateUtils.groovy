#!/usr/bin/env groovy
package org.ops.util

static def validateRequiredParams(Object obj,List<String> keys) {
    keys.each { t ->
        if (StringUtils.isEmpty(obj.getProperty(t))) {
            error "${t} must be not empty"
        }
    }
}

return this