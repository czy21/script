#!/usr/bin/env python3
import logging
import pathlib

from domain import base
from utility import db as db_util, collection as list_util, basic as basic_util, file as file_util

logger = logging.getLogger()

mssql_cmd = "sqlcmd"

createTimeColumn = "create_time datetime NOT NULL DEFAULT GETDATE()"
createUserColumn = "create_user varchar(36)  NULL"
updateTimeColumn = "update_time datetime NOT NULL DEFAULT GETDATE()"
updateUserColumn = "update_user varchar(36)  NULL"
deletedColumn = "deleted bit NOT NULL DEFAULT 0"

class MsSQLSource(base.AbstractDBSource):

    def __init__(self, context: base.ExecutionContext) -> None:
        super().__init__(context)
        self.host = self.context.param.param_main_db_mssql_host
        self.port = self.context.param.param_main_db_mssql_port
        self.username = self.context.param.param_main_db_mssql_username
        self.password = self.context.param.param_main_db_mssql_password
        self.database = self.context.param.param_main_db_mssql_database

    def key(self) -> str:
        return 'mssql'
    
    def meta(self):
        return {
            "header": "SELECT 'executing: {{ file_path }}' AS [file];",
            "footer": "SELECT 'executed: {{ file_path }}' AS [file];",
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
            f"-S {self.host},{self.port}",
            f"-U {self.username}",
            f"-P {self.password}",
            "-f 65001 -b -r -j"
        ]
        if with_database:
            param.append(f"-d {self.database}")
        return list_util.flat_to_str(param)

    def get_recreate_command(self) -> str:
        return list_util.flat_to_str(mssql_cmd, self.get_basic_param(False), [
            "-Q \"{0}\"".format("".join(
                [
                    "declare @db_name varchar(100);set @db_name = (SELECT name FROM Master.dbo.SysDatabases where name = '{0}');".format(self.database),
                    "if @db_name is not null ALTER DATABASE {0} SET SINGLE_USER WITH ROLLBACK IMMEDIATE;".format(self.database),
                    "drop database if exists {0};".format(self.database),
                    "create database {0};".format(self.database)
                ])
            )
        ])

    def recreate(self) -> None:
        command = self.get_recreate_command()
        basic_util.execute(command)

    def execute(self) -> None:
        command = list_util.flat_to_str(mssql_cmd, self.get_main_db_param_dict(), [
            "-e",
            "-i \"{0}\"".format(pathlib.Path(self.context.param.output_db_all_in_one_mssql).__fspath__())
        ])
        basic_util.execute(command, db_util.print_ql_msg)