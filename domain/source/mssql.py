#!/usr/bin/env python3
import logging
import pathlib
from pathlib import Path

from domain.db_meta import mssql as mssql_meta
from domain.default import common as default_common
from domain.default import path as default_path
from utility import db as db_util, collection as list_util, basic as basic_util

logger = logging.getLogger()

mssql_cmd = "sqlcmd"


def assemble() -> None:
    db_util.assemble_ql(pathlib.Path(default_common.param_main_db_mssql_file_path), pathlib.Path(default_path.output_db_all_in_one_mssql), mssql_meta, "sql")


def recreate() -> None:
    command = get_recreate_command(default_common.param_main_db_mssql_host,
                                   default_common.param_main_db_mssql_port,
                                   default_common.param_main_db_mssql_user,
                                   default_common.param_main_db_mssql_pass,
                                   default_common.param_main_db_name)
    basic_util.execute(command)


def get_basic_param(host, port, user, password, db_name) -> str:
    param = [
        "-S {0},{1}".format(host, port),
        "-U " + user,
        "-P " + password,
        "-f 65001 -b -r -j"
    ]
    if db_name:
        param.append("-d " + db_name)
    return list_util.flat_to_str(param)


def get_main_db_param_dict() -> str:
    return get_basic_param(default_common.param_main_db_mssql_host,
                           default_common.param_main_db_mssql_port,
                           default_common.param_main_db_mssql_user,
                           default_common.param_main_db_mssql_pass,
                           default_common.param_main_db_name)


def execute() -> None:
    extra_param_dict = [
        "-e",
        "-i \"{0}\"".format(Path(default_path.output_db_all_in_one_mssql).__fspath__())
    ]
    command = list_util.flat_to_str(mssql_cmd, get_main_db_param_dict(), extra_param_dict)
    basic_util.execute(command, db_util.print_ql_msg)


def get_recreate_command(host, port, user, password, db_name) -> str:
    extra_param = [
        "-Q \"{0}\"".format("".join(
            [
                "declare @db_name varchar(100);set @db_name = (SELECT name FROM Master.dbo.SysDatabases where name = '{0}');".format(db_name),
                "if @db_name is not null ALTER DATABASE {0} SET SINGLE_USER WITH ROLLBACK IMMEDIATE;".format(db_name),
                "drop database if exists {0};".format(db_name),
                "create database {0};".format(db_name)
            ])
        )
    ]
    return list_util.flat_to_str(mssql_cmd, get_basic_param(host, port, user, password, None), extra_param)
