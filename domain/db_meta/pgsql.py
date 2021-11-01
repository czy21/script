#!/usr/bin/env python3

self = {
    "header": "SELECT 'executing: ${{{file_path}}}' AS file;",
    "footer": "SELECT 'executed: ${{{file_path}}}' AS file;",
    "substitution": {
        "TrackedColumns": "\tcreated_date  timestamp(6) DEFAULT CURRENT_TIMESTAMP,\n"
                          "\tcreated_user  varchar(36) DEFAULT NULL,\n"
                          "\tmodified_date timestamp(6) DEFAULT CURRENT_TIMESTAMP,\n"
                          "\tmodified_user varchar(36) DEFAULT NULL"
    }
}
