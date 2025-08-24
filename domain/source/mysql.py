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

    def assemble(self) -> None:
        db_util.assemble_ql(pathlib.Path(self.context.param.param_main_db_mysql_file_path), pathlib.Path(self.context.param.output_db_all_in_one_mysql), mysql_meta, "sql")

    def recreate(self) -> None:
        command = self.get_recreate_command(self.context.param.param_main_db_mysql_host,
                                            self.context.param.param_main_db_mysql_port,
                                            self.context.param.param_main_db_mysql_username,
                                            self.context.param.param_main_db_mysql_password,
                                            self.context.param.param_main_db_mysql_database)
        basic_util.execute(command)

    def get_basic_param(self, host, port, user, password, db_name) -> str:
        param = ["--default-character-set=utf8mb4",
                 "--host=" + host,
                 "--port=" + port,
                 "--user=" + user,
                 "--password=" + password
                 ]
        if db_name:
            param.append("--database=" + db_name)
        return list_util.flat_to_str(param)

    def get_main_db_param_dict(self) -> str:
        return self.get_basic_param(self.context.param.param_main_db_mysql_host,
                                    self.context.param.param_main_db_mysql_port,
                                    self.context.param.param_main_db_mysql_username,
                                    self.context.param.param_main_db_mysql_password,
                                    self.context.param.param_main_db_mysql_database)

    def execute(self) -> None:
        extra_param_dict = [
            "--skip-column-names",
            "< " + self.context.param.output_db_all_in_one_mysql
        ]
        command = list_util.flat_to_str([mysql_cmd, self.get_main_db_param_dict(), extra_param_dict])
        basic_util.execute(command, db_util.print_ql_msg)

    def get_recreate_command(self, host, port, user, password, db_name) -> str:
        extra_param = [
            "--execute \"{0}\"".format("".join(
                [
                    "drop database if exists {0};".format(db_name),
                    "create database if not exists {0} default charset utf8mb4 collate utf8mb4_unicode_ci;".format(db_name),
                ])
            )
        ]
        return list_util.flat_to_str([mysql_cmd, self.get_basic_param(host, port, user, password, None), extra_param])

    def backup_db(self) -> None:
        recreate_command = self.get_recreate_command(self.context.param.param_main_db_mysql_host,
                                                     self.context.param.param_main_db_mysql_port,
                                                     self.context.param.param_main_db_mysql_username,
                                                     self.context.param.param_main_db_mysql_password,
                                                     self.context.param.param_main_db_bak_name)
        command = list_util.flat_to_str(recreate_command,
                                        "&&mysqldump",
                                        list_util.flat_to_str([
                                            self.get_basic_param(self.context.param.param_main_db_mysql_host,
                                                                 self.context.param.param_main_db_mysql_port,
                                                                 self.context.param.param_main_db_mysql_username,
                                                                 self.context.param.param_main_db_mysql_password, None),
                                            "--opt",
                                            self.context.param.param_main_db_mysql_database,
                                            "--max-allowed-packet=1024M"
                                        ]),
                                        "| mysql",
                                        list_util.flat_to_str([
                                            self.get_basic_param(self.context.param.param_main_db_mysql_host,
                                                                 self.context.param.param_main_db_mysql_port,
                                                                 self.context.param.param_main_db_mysql_username,
                                                                 self.context.param.param_main_db_mysql_password,
                                                                 None),
                                            "--compress",
                                            self.context.param.param_main_db_bak_name,
                                        ]))
        basic_util.execute(command)

    def backup_sql(self) -> None:
        command = list_util.flat_to_str("mysqldump",
                                        list_util.flat_to_str([
                                            self.get_basic_param(self.context.param.param_main_db_mysql_host,
                                                                 self.context.param.param_main_db_mysql_port,
                                                                 self.context.param.param_main_db_mysql_username,
                                                                 self.context.param.param_main_db_mysql_password, None),
                                            "--opt",
                                            self.context.param.param_main_db_mysql_database,
                                        ]),
                                        "--skip-opt",
                                        "--complete-insert",
                                        " > ",
                                        self.context.param.output_db_bak_sql_mysql
                                        )
        basic_util.execute(command)

    def backup_gz(self) -> None:
        command = list_util.flat_to_str("mysqldump",
                                        list_util.flat_to_str([
                                            self.get_basic_param(self.context.param.param_main_db_mysql_host,
                                                                 self.context.param.param_main_db_mysql_port,
                                                                 self.context.param.param_main_db_mysql_username,
                                                                 self.context.param.param_main_db_mysql_password, None),
                                            "--opt",
                                            self.context.param.param_main_db_mysql_database,
                                        ]),
                                        "| gzip > ",
                                        self.context.param.output_db_bak_gz_mysql
                                        )
        basic_util.execute(command)

    def restore_gz(self) -> None:
        recreate_command = self.get_recreate_command(self.context.param.param_main_db_mysql_host,
                                                     self.context.param.param_main_db_mysql_port,
                                                     self.context.param.param_main_db_mysql_username,
                                                     self.context.param.param_main_db_mysql_password,
                                                     self.context.param.param_main_db_mysql_database)
        command = list_util.flat_to_str(recreate_command,
                                        "&& gzip -d < ",
                                        self.context.param.output_db_bak_gz_mysql,
                                        "| mysql",
                                        list_util.flat_to_str([
                                            self.get_basic_param(self.context.param.param_main_db_mysql_host,
                                                                 self.context.param.param_main_db_mysql_port,
                                                                 self.context.param.param_main_db_mysql_username,
                                                                 self.context.param.param_main_db_mysql_password,
                                                                 self.context.param.param_main_db_mysql_database)
                                        ]))
        basic_util.execute(command)
