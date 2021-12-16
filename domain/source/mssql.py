#!/usr/bin/env python3
import inspect
import os
from pathlib import Path

from script.domain.db_meta import mssql as mssql_meta
from script.domain.default import common as default_common
from script.domain.default import path as default_path
from script.utility import db as db_util, collection as list_util, basic as basic_util, path as path_util, log

logger = log.Logger(__name__)

mssql_cmd = "sqlcmd"


def __get_function_name():
    return inspect.stack()[1][3]


def assemble() -> None:
    db_util.assemble_ql(default_common.param_main_db_mssql_file_path, default_path.output_db_all_in_one_mssql, mssql_meta, "sql")


def recreate() -> None:
    command = get_recreate_command(default_common.param_main_db_mssql_host,
                                   default_common.param_main_db_mssql_port,
                                   default_common.param_main_db_mssql_user,
                                   default_common.param_main_db_mssql_pass,
                                   default_common.param_main_db_name)
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)


def get_basic_param(host, port, user, password, db_name) -> str:
    param = [
        "-S {0},{1}".format(host, port),
        "-U " + user,
        "-P " + password
    ]
    if db_name:
        param.append("-d " + db_name)
    return list_util.arr_param_to_str(param)


def get_main_db_param_dict() -> str:
    return get_basic_param(default_common.param_main_db_mssql_host,
                           default_common.param_main_db_mssql_port,
                           default_common.param_main_db_mssql_user,
                           default_common.param_main_db_mssql_pass,
                           default_common.param_main_db_name)


def execute() -> None:
    extra_param_dict = [
        "-e",
        "-i \"{0}\"".format(Path(default_path.output_db_all_in_one_mssql).__fspath__() if os.name == 'nt' else default_path.output_db_all_in_one_mssql)
    ]
    command = list_util.arr_param_to_str(mssql_cmd, get_main_db_param_dict(), extra_param_dict)
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command, db_util.print_ql_msg)


def get_recreate_command(host, port, user, password, db_name) -> str:
    extra_param_dict = [
        "-Q",
        "\"",
        "declare @db_name varchar(100);set @db_name = (SELECT name FROM Master.dbo.SysDatabases where name = '{0}');".format(db_name),
        "if @db_name is not null ALTER DATABASE {0} SET SINGLE_USER WITH ROLLBACK IMMEDIATE;".format(db_name),
        "drop database if exists {0};".format(db_name),
        "create database {0};".format(db_name),
        "\""
    ]
    return list_util.arr_param_to_str(mssql_cmd, get_basic_param(host, port, user, password, None), extra_param_dict)
