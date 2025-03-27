package org.ops


import org.ops.util.PathUtils
import org.ops.util.StringUtils

def deploy() {
    def start_api_file = ".jenkins/start-api.sh"
    def content = libraryResource "org/ops/start-api.sh"
    writeFile file: start_api_file, text: content, encoding: 'utf-8'
}

return this