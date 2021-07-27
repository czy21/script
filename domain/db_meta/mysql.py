#!/usr/bin/env python3

self = {
    "header": "SELECT 'executing: ${{{file_path}}}' AS file;",
    "footer": "SELECT 'executed: ${{{file_path}}}' AS file;",
    "substitution": {
        "TrackedColumns": "\t`created_date` TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),\n"
                          "\t`created_user` varchar(36) DEFAULT NULL,\n"
                          "\t`modified_date` TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),\n"
                          "\t`modified_user` varchar(36) DEFAULT NULL"
    }
}
