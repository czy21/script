#!/usr/bin/env python3

self = {
    "header": "SELECT 'executing: {{ file_path }}' AS file;",
    "footer": "SELECT 'executed: {{ file_path }}' AS file;",
    "substitution": {
        "TrackColumn": "\tcreate_time  timestamp(6) DEFAULT CURRENT_TIMESTAMP,\n"
                          "\tcreate_user  varchar(36)  DEFAULT NULL,\n"
                          "\tupdate_time  timestamp(6) DEFAULT CURRENT_TIMESTAMP,\n"
                          "\tupdate_user  varchar(36)  DEFAULT NULL,\n"
                          "\tdeleted bool NOT NULL DEFAULT 'n'"
    }
}
