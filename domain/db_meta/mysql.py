#!/usr/bin/env python3

self = {
    "header": "SELECT 'executing: ${{{file_path}}}' AS file;",
    "footer": "SELECT 'executed: ${{{file_path}}}' AS file;",
    "substitution": {
        "TrackedColumns": "`created_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,\n"
                          "\t`created_user` varchar(36) DEFAULT NULL,\n"
                          "\t`modified_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,\n"
                          "\t`modified_user` varchar(36) DEFAULT NULL"
    }
}
