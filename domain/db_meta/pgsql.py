#!/usr/bin/env python3

createTimeColumn = "create_time  timestamp(6) DEFAULT CURRENT_TIMESTAMP"
createUserColumn = "create_user  varchar(36)  DEFAULT NULL"
updateTimeColumn = "update_time  timestamp(6) DEFAULT CURRENT_TIMESTAMP"
updateUserColumn = "update_user  varchar(36)  DEFAULT NULL"
deletedColumn = "deleted bool NOT NULL DEFAULT 'n'"

self = {
    "header": "SELECT 'executing: {{ file_path }}' AS file;",
    "footer": "SELECT 'executed: {{ file_path }}' AS file;",
    "substitution": {
        "CreateTimeColumn": "\t{0}".format(createTimeColumn),
        "CreateUserColumn": "\t{0}".format(createUserColumn),
        "UpdateTimeColumn": "\t{0}".format(updateTimeColumn),
        "UpdateUserColumn": "\t{0}".format(updateUserColumn),
        "DeletedColumn": "\t{0}".format(deletedColumn),
        "TrackColumn": ",\n".join(["\t{0}".format(t) for t in [createTimeColumn, createUserColumn, updateTimeColumn, updateUserColumn, deletedColumn]]),
    }
}
