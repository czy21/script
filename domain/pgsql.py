#!/usr/bin/env python3
import logging
import pathlib

from domain import base
from utility import db as db_util, collection as list_util, basic as basic_util, file as file_util

logger = logging.getLogger()

pgsql_cmd = "psql"
pgsqldump = "pg_dump"

createTimeColumn = "create_time  timestamp(6) DEFAULT CURRENT_TIMESTAMP"
createUserColumn = "create_user  varchar(36)  DEFAULT NULL"
updateTimeColumn = "update_time  timestamp(6) DEFAULT CURRENT_TIMESTAMP"
updateUserColumn = "update_user  varchar(36)  DEFAULT NULL"
deletedColumn = "deleted bool NOT NULL DEFAULT 'n'"

class PgSQLSource(base.AbstractDBSource):

    def __init__(self, context: base.ExecutionContext) -> None:
        super().__init__(context)
        self.host = self.context.param.param_main_db_pgsql_host
        self.port = self.context.param.param_main_db_pgsql_port
        self.username = self.context.param.param_main_db_pgsql_username
        self.password = self.context.param.param_main_db_pgsql_password
        self.database = self.context.param.param_main_db_pgsql_database
        self.output_db_all_in_one = pathlib.Path(self.context.param.output_db_all,f'pgsql-{self.database}.sql').as_posix()
        self.output_db_bak_gz = pathlib.Path(self.context.param.output_db_bak).joinpath(f'pgsql-{self.database}.gz').as_posix()

    def key(self): -> str:
        return 'pgsql'

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
            f"--host={self.host}",
            f"--port={self.port}",
            f"--username={self.username}"
        ]
        if with_database:
            param.append(f"--dbname={self.database}")
        return list_util.flat_to_str(param)

    def get_recreate_command(self) -> str:
        cmd = [
            "echo \"{0}\"".format("".join(
                [
                    "drop database if exists {0} WITH (FORCE);".format(self.database),
                    "CREATE DATABASE {} WITH OWNER = postgres ENCODING = \'UTF8\' CONNECTION LIMIT = -1;".format(self.database),
                ])
            ),
            "|",
            f"PGPASSWORD={self.password}",
            pgsql_cmd,
            self.get_basic_param(False)
        ]
        return list_util.flat_to_str(cmd)

    def recreate(self) -> None:
        command = self.get_recreate_command()
        basic_util.execute(command)

    def execute(self) -> None:
        command = list_util.flat_to_str(
            f"PGPASSWORD={self.password}",
            pgsql_cmd,
            self.get_basic_param(True),
            f"< {self.context.param.output_db_all_in_one}"
        )
        basic_util.execute(command, db_util.print_ql_msg, encoding="gbk" if os.name == 'nt' else "utf-8")

    def backup(self) -> None:
        cmd = list_util.flat_to_str([
            f"PGPASSWORD={self.password}",
            pgsqldump,
            self.get_basic_param(True),
            "--column-inserts",
            f"| gzip > {self.context.param.output_db_bak_gz}"
        ])
        basic_util.execute(cmd)
