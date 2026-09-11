#!/usr/bin/env python3
import logging
import pathlib

from domain import base
from utility import db as db_util, collection as list_util, basic as basic_util

logger = logging.getLogger()

mysql_cmd = "mysql"
mysqldump = "mysqldump"

createTimeColumn = "create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'"
createUserColumn = "create_user varchar(255) NULL COMMENT '创建人'"
updateTimeColumn = "update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'"
updateUserColumn = "update_user varchar(255) NULL COMMENT '更新人'"
deletedColumn = "deleted bit(1) NOT NULL DEFAULT b'0' COMMENT '是否删除'"


class MySQLSource(base.AbstractDBSource):

    def __init__(self, context: base.ExecutionContext):
        super().__init__(context)
        self.host = self.context.param.param_main_db_mysql_host
        self.port = self.context.param.param_main_db_mysql_port
        self.username = self.context.param.param_main_db_mysql_username
        self.password = self.context.param.param_main_db_mysql_password
        self.database = self.context.param.param_main_db_mysql_database

        self.out_db_ql = pathlib.Path(self.context.param.out_path).joinpath(f'{self.key()}-{self.database}.sql').as_posix()

        self.out_db_bak_ql = pathlib.Path(self.context.param.out_path).joinpath(f'{self.key()}-{self.database}-bak.sql').as_posix()
        self.out_db_bak_gz = pathlib.Path(self.context.param.out_path).joinpath(f'{self.key()}-{self.database}-bak.gz').as_posix()

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

    def _source_param(self, with_database=False) -> str:
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
        ql = [
            f'drop database if exists {self.database};',
            f'create database if not exists {self.database} default charset utf8mb4 collate utf8mb4_unicode_ci;'
        ]
        return f'{mysql_cmd} {self._source_param(False)} --execute \'{"".join(ql)}\''

    def recreate(self) -> None:
        basic_util.execute(self.get_recreate_command())

    def execute(self) -> None:
        basic_util.execute(f'{mysql_cmd} {self._source_param(True)} --skip-column-names < {self.out_db_ql}', db_util.print_ql_msg)

    def backup(self) -> None:
        basic_util.execute(f'{mysqldump} {self._source_param(False)} --databases {self.database} | gzip > {self.out_db_bak_gz}')

    def restore(self) -> None:
        basic_util.execute(self.get_recreate_command())
        basic_util.execute(f'gzip -d < {self.out_db_bak_gz} | {mysql_cmd} {self._source_param(True)}')
