package org.ops


import org.ops.util.PathUtils
import org.ops.util.StringUtils

def deploy() {
    
    def archive_file = ".jenkins/host-archive.sh"
    def archive_content = libraryResource "org/ops/host-archive.sh"
    writeFile file: archive_file, text: archive_content, encoding: 'utf-8'

    def start_api_file = ".jenkins/host-start-api.sh"
    def start_api_content = libraryResource "org/ops/host-start-api.sh"
    writeFile file: start_api_file, text: start_api_content, encoding: 'utf-8'

    sh "chmod +x ${archive_file};${archive_file}"
}

return this