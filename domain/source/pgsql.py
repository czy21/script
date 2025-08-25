#!/usr/bin/env python3
import logging
import os
import pathlib

from domain.meta import pgsql as pgsql_meta
from domain.source import base as base_source
from utility import db as db_util, collection as list_util, basic as basic_util

logger = logging.getLogger()

psql_cmd = "psql"
pg_dump_cmd = "pg_dump"


class PgSQLSource(base_source.AbstractSource):

    def __init__(self, context: base_source.ExecutionContext) -> None:
        super().__init__(context)
        self.host = self.context.param.param_main_db_pgsql_host
        self.port = self.context.param.param_main_db_pgsql_port
        self.username = self.context.param.param_main_db_pgsql_username
        self.password = self.context.param.param_main_db_pgsql_password
        self.database = self.context.param.param_main_db_pgsql_database

    def assemble(self) -> None:
        db_util.assemble_ql(pathlib.Path(self.context.param.param_main_db_pgsql_file_path), pathlib.Path(self.context.param.output_db_all_in_one_pgsql), pgsql_meta, "sql")

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
            psql_cmd,
            self.get_basic_param(False)
        ]
        return list_util.flat_to_str(cmd)

    def recreate(self) -> None:
        command = self.get_recreate_command()
        basic_util.execute(command)

    def execute(self) -> None:
        command = list_util.flat_to_str(
            f"PGPASSWORD={self.password}",
            psql_cmd,
            self.get_basic_param(True),
            f"< {self.context.param.output_db_all_in_one_pgsql}"
        )
        basic_util.execute(command, db_util.print_ql_msg, encoding="gbk" if os.name == 'nt' else "utf-8")

    def backup(self) -> None:
        cmd = list_util.flat_to_str([
            f"PGPASSWORD={self.password}",
            pg_dump_cmd,
            self.get_basic_param(True),
            "--column-inserts",
            f"| gzip > {self.context.param.output_db_bak_gz_pgsql}"
        ])
        basic_util.execute(cmd)
