#!/usr/bin/env python3
import logging
import pathlib

from domain import base
from utility import db as db_util, collection as list_util, basic as basic_util, file as file_util

logger = logging.getLogger()

mysql_cmd = "mysql"
mysqldump = "mysqldump"

createTimeColumn = "create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'"
createUserColumn = "create_user varchar(255) NULL COMMENT '创建人'"
updateTimeColumn = "update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'"
updateUserColumn = "update_user varchar(255) NULL COMMENT '更新人'"
deletedColumn = "deleted bit(1) NOT NULL DEFAULT b'0' COMMENT '是否删除'"

class MySQLSource(base.AbstractDBSource):

    def __init__(self, context: base.ExecutionContext) -> None:
        super().__init__(context)
        self.host = self.context.param.param_main_db_mysql_host
        self.port = self.context.param.param_main_db_mysql_port
        self.username = self.context.param.param_main_db_mysql_username
        self.password = self.context.param.param_main_db_mysql_password
        self.database = self.context.param.param_main_db_mysql_database
        self.output_db_all_in_one = pathlib.Path(self.context.param.output_db_all,f'mysql-{self.database}.sql').as_posix()
        self.output_db_bak_gz = pathlib.Path(self.context.param.output_db_bak).joinpath(f'mysql-{self.database}.gz').as_posix()

    def key(self) -> str:
        return 'mysql'
    
    def meta(self):
        return {
            "header": "SELECT 'executing: {{ file_path }}' AS file;",
            "footer": "SELECT 'executed: {{ file_path }}' AS file;",
            "substitution": {
                "CreateTimeColumn": "{0}".format(createTimeColumn),
                "CreateUserColumn": "{0}".format(createUserColumn),
                "UpdateTimeColumn": "{0}".format(updateTimeColumn),
                "UpdateUserColumn": "{0}".format(updateUserColumn),
                "DeletedColumn": "{0}".format(deletedColumn),
                "TrackedColumn": ",".join(["{0}".format(t) for t in [createTimeColumn, createUserColumn, updateTimeColumn, updateUserColumn, deletedColumn]]),
            }
        }

    def get_basic_param(self, with_database=False) -> str:
        param = [
            "--default-character-set=utf8mb4",
            f"--host={self.host}",
            f"--port={self.port}",
            f"--user={self.username}",
            f"--password={self.password}"
        ]
        if with_database:
            param.append(f"--database={self.database}")
        return list_util.flat_to_str(param)

    def get_recreate_command(self) -> str:
        return list_util.flat_to_str([mysql_cmd, self.get_basic_param(False), [
            "--execute \"{0}\"".format("".join(
                [
                    "drop database if exists {0};".format(self.database),
                    "create database if not exists {0} default charset utf8mb4 collate utf8mb4_unicode_ci;".format(self.database),
                ])
            )
        ]])

    def recreate(self) -> None:
        command = self.get_recreate_command()
        basic_util.execute(command)

    def execute(self) -> None:
        command = list_util.flat_to_str([mysql_cmd, self.get_basic_param(True), [
            "--skip-column-names",
            f"< {self.output_db_all_in_one}"
        ]])
        basic_util.execute(command, db_util.print_ql_msg)

    def backup(self) -> None:
        command = list_util.flat_to_str("mysqldump",
                                        self.get_basic_param(False),
                                        f"--databases {self.database}",
                                        f"| gzip > {self.context.output_db_bak_gz}"
                                        )
        basic_util.execute(command)

    def restore(self) -> None:
        command = list_util.flat_to_str(self.get_recreate_command(),
                                        f"&& gzip -d < {self.context.output_db_bak_gz}",
                                        "| mysql", self.get_basic_param(True)
                                        )
        basic_util.execute(command)
