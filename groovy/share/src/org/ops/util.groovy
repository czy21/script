@Grab('org.apache.commons:commons-lang3:3.12.0')
import org.apache.commons.lang3.StringUtils

def isEmptyWithNullString() {
  return StringUtils.isEmpty(c) || c.equals("null")
}

return this