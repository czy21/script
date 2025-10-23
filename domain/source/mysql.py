#!/usr/bin/env python3
import logging
import pathlib

from domain.meta import mysql as mysql_meta
from domain.source import base as base_source
from utility import db as db_util, collection as list_util, basic as basic_util, file as file_util

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
        everyone_prep_content = db_util.assemble_ql(pathlib.Path(self.context.param.param_main_db_mysql_everyone_path).joinpath("prep"), mysql_meta, "sql")
        version_content = db_util.assemble_ql(pathlib.Path(self.context.param.param_main_db_mysql_version_path), mysql_meta, "sql")
        everyone_post_content = db_util.assemble_ql(pathlib.Path(self.context.param.param_main_db_mysql_everyone_path).joinpath("post"), mysql_meta, "sql")
        file_util.write_text(pathlib.Path(self.output_db_all_in_one_mysql), u'{}'.format("\n\n".join([*everyone_prep_content,*version_content,*everyone_post_content])))

    def assemble_release(self) -> None:
        everyone_prep_content = db_util.assemble_ql(pathlib.Path(self.context.param.param_main_db_mysql_everyone_path).joinpath("prep"), mysql_meta, "sql")
        version_file = pathlib.Path(self.context.param.version_file)
        release_path = None
        release_name = self.context.param.get('param_main_db_mysql_release_name',f"release-{version_file.read_text()}" if version_file.exists() else "")
        release_path = pathlib.Path(self.context.param.param_main_db_mysql_version_path).joinpath(release_name)
        if not self.context.param.get('param_main_db_mysql_release_name') and not version_file.exists():
            raise Exception(f"param_main_db_mysql_release_name must be not null")
        if not release_path.exists():
            raise Exception(f"{release_path.as_posix()} not exist")
        release_content = db_util.assemble_ql(release_path, mysql_meta, "sql")
        everyone_post_content = db_util.assemble_ql(pathlib.Path(self.context.param.param_main_db_mysql_everyone_path).joinpath("post"), mysql_meta, "sql")
        file_util.write_text(pathlib.Path(self.output_db_all_in_one_mysql), u'{}'.format("\n\n".join([*everyone_prep_content,*release_content,*everyone_post_content])))

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
