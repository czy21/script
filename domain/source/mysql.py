#!/usr/bin/env python3
import logging
import pathlib

from domain.meta import mysql as mysql_meta
from domain.source import base as base_source
from utility import db as db_util, collection as list_util, basic as basic_util

logger = logging.getLogger()
mysql_cmd = "mysql"


class MySQLSource(base_source.AbstractSource):

    def __init__(self, context: base_source.ExecutionContext) -> None:
        super().__init__(context)
        self.host = self.context.param.param_main_db_mysql_host
        self.port = self.context.param.param_main_db_mysql_port
        self.username = self.context.param.param_main_db_mysql_username
        self.password = self.context.param.param_main_db_mysql_password
        self.database = self.context.param.param_main_db_mysql_database
        self.output_db_all_in_one_mysql = pathlib.Path(self.context.param.output_db_all_in_one,f'mysql-{self.database}.sql').as_posix()
        self.output_db_bak_gz_mysql = pathlib.Path(self.context.param.output_db_bak).joinpath(f'mysql-{self.database}.gz').as_posix()

    def assemble(self) -> None:
        db_util.assemble_ql(pathlib.Path(self.context.param.param_main_db_mysql_file_path), pathlib.Path(self.output_db_all_in_one_mysql), mysql_meta, "sql")

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
            f"< {self.output_db_all_in_one_mysql}"
        ]])
        basic_util.execute(command, db_util.print_ql_msg)

    def backup(self) -> None:
        command = list_util.flat_to_str("mysqldump",
                                        self.get_basic_param(False),
                                        f"--databases {self.database}",
                                        f"| gzip > {self.context.output_db_bak_gz_mysql}"
                                        )
        basic_util.execute(command)

    def restore(self) -> None:
        command = list_util.flat_to_str(self.get_recreate_command(),
                                        f"&& gzip -d < {self.context.output_db_bak_gz_mysql}",
                                        "| mysql", self.get_basic_param(True)
                                        )
        basic_util.execute(command)
