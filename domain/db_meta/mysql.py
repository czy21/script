#!/usr/bin/env python3

self = {
    "header": "SELECT 'executing: {{ file_path }}' AS file;",
    "footer": "SELECT 'executed: {{ file_path }}' AS file;",
    "substitution": {
        "TrackedColumns": "\tcreate_time  datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',\n"
                          "\tcreate_user  varchar(64)  NULL COMMENT '创建人',\n"
                          "\tupdate_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',\n"
                          "\tupdate_user varchar(64)   NULL  COMMENT '更新人',\n"
                          "\tdeleted bit(1) NOT NULL DEFAULT b'0' COMMENT '是否删除'"
    }
}
