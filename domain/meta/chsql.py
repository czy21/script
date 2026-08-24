#!/usr/bin/env python3

createTimeColumn = "create_time TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6)"
createUserColumn = "create_user varchar(36) DEFAULT NULL"
updateTimeColumn = "update_time TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"
updateUserColumn = "update_user varchar(36) DEFAULT NULL"

self = {
    "header": "SELECT 'executing: {{ file_path }}' AS file;",
    "footer": "SELECT 'executed: {{ file_path }}' AS file;",
    "substitution": {
        "CreateTimeColumn": "{0}".format(createTimeColumn),
        "CreateUserColumn": "{0}".format(createUserColumn),
        "UpdateTimeColumn": "{0}".format(updateTimeColumn),
        "UpdateUserColumn": "{0}".format(updateUserColumn),
        "TrackedColumn": ",".join(["{0}".format(t) for t in [createTimeColumn, createUserColumn, updateTimeColumn, updateUserColumn]]),
    }
}