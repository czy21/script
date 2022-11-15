#!/usr/bin/env python3
import logging
import pathlib

from domain.db_meta import chsql as chsql_meta
from domain.default import common as default_common
from domain.default import path as default_path
from utility import db as db_util, collection as list_util, basic as basic_util

logger = logging.getLogger()

chsql_cmd = "mysql"


def assemble() -> None:
    db_util.assemble_ql(pathlib.Path(default_common.param_main_db_chsql_file_path), pathlib.Path(default_path.output_db_all_in_one_chsql), chsql_meta, "sql")


def recreate() -> None:
    command = get_recreate_command(default_common.param_main_db_chsql_host,
                                   default_common.param_main_db_chsql_port,
                                   default_common.param_main_db_chsql_user,
                                   default_common.param_main_db_chsql_pass,
                                   default_common.param_main_db_name)
    basic_util.execute(command)


def get_basic_param(host, port, user, password, db_name) -> str:
    param = ["--default-character-set=utf8mb4",
             "--host=" + host,
             "--port=" + port,
             "--user=" + user,
             "--password=" + password
             ]
    if db_name:
        param.append("--database=" + db_name)
    return list_util.flat_to_str(param)


def get_main_db_param_dict() -> str:
    return get_basic_param(default_common.param_main_db_chsql_host,
                           default_common.param_main_db_chsql_port,
                           default_common.param_main_db_chsql_user,
                           default_common.param_main_db_chsql_pass,
                           default_common.param_main_db_name)


def execute() -> None:
    extra_param_dict = [
        "--skip-column-names",
        "< " + default_path.output_db_all_in_one_chsql
    ]
    command = list_util.flat_to_str(chsql_cmd, get_main_db_param_dict(), extra_param_dict)
    basic_util.execute(command, db_util.print_ql_msg)


def get_recreate_command(host, port, user, password, db_name) -> str:
    extra_param_dict = [
        "--execute",
        "\"",
        "drop database if exists {0};".format(db_name),
        "create database if not exists {0} ENGINE = Atomic;".format(db_name),
        "\""
    ]
    return list_util.flat_to_str(chsql_cmd, get_basic_param(host, port, user, password, None), extra_param_dict)
