#!/usr/bin/env python3

self = {
    "header": "SELECT 'executing: ${{{file_path}}}' AS file;",
    "footer": "SELECT 'executed: ${{{file_path}}}' AS file;",
    "substitution": {
        "TrackedColumns": "\tcreate_time TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6),\n"
                          "\tcreate_user varchar(36) DEFAULT NULL,\n"
                          "\tupdate_time TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),\n"
                          "\tupdate_user varchar(36) DEFAULT NULL"
    }
}
