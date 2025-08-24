#!/usr/bin/env python3
createTimeColumn = "create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'"
createUserColumn = "create_user varchar(36)  NULL COMMENT '创建人'"
updateTimeColumn = "update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'"
updateUserColumn = "update_user varchar(36)  NULL COMMENT '更新人'"
deletedColumn = "deleted bit(1) NOT NULL DEFAULT b'0' COMMENT '是否删除'"
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
