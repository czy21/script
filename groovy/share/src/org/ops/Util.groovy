#!/usr/bin/env groovy
package org.ops
@Grab('org.apache.commons:commons-lang3:3.12.0')
import org.apache.commons.lang3.StringUtils

def isEmptyWithNullString(String str) {
  return StringUtils.isEmpty(str) || str.equals("null")
}

return this