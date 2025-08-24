#!/usr/bin/env python3

self = {
    "header": "SELECT 'executing: {{ file_path }}' AS file;",
    "footer": "SELECT 'executed: {{ file_path }}' AS file;",
    "substitution": {
        "TrackedColumns": "\tcreated_date  TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6),\n"
                          "\tcreated_user  varchar(36) DEFAULT NULL,\n"
                          "\tmodified_date TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),\n"
                          "\tmodified_user varchar(36) DEFAULT NULL"
    }
}
