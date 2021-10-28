#!/usr/bin/env python3

self = {
    "header": "SELECT 'executing: ${{{file_path}}}' AS file;",
    "footer": "SELECT 'executed: ${{{file_path}}}' AS file;",
    "substitution": {
        "TrackedColumns": "\tcreate_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,\n"
                          "\tcreate_user varchar(36) DEFAULT NULL,\n"
                          "\tupdate_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,\n"
                          "\tupdate_user varchar(36) DEFAULT NULL"
    }
}
