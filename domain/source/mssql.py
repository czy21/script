#!/usr/bin/env python3
import logging
import pathlib
from pathlib import Path

from domain.meta import mssql as mssql_meta
from domain.source import base as base_source
from utility import db as db_util, collection as list_util, basic as basic_util

logger = logging.getLogger()

mssql_cmd = "sqlcmd"


class MsSQLSource(base_source.AbstractSource):

    def __init__(self, context: base_source.ExecutionContext) -> None:
        super().__init__(context)
        self.host = self.context.param.param_main_db_mssql_host
        self.port = self.context.param.param_main_db_mssql_port
        self.username = self.context.param.param_main_db_mssql_username
        self.password = self.context.param.param_main_db_mssql_password
        self.database = self.context.param.param_main_db_mssql_database

    def assemble(self) -> None:
        db_util.assemble_ql(pathlib.Path(self.context.param.param_main_db_mssql_file_path), pathlib.Path(self.context.param.output_db_all_in_one_mssql), mssql_meta, "sql")

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
            "-i \"{0}\"".format(Path(self.context.param.output_db_all_in_one_mssql).__fspath__())
        ])
        basic_util.execute(command, db_util.print_ql_msg)