#!/usr/bin/env python3
import inspect
import pathlib

from domain.db_meta import cksql as cksql_meta
from domain.default import common as default_common
from domain.default import path as default_path
from utility import db as db_util, collection as list_util, basic as basic_util, log

logger = log.Logger(__name__)

cksql_cmd = "mysql"


def __get_function_name():
    return inspect.stack()[1][3]


def assemble() -> None:
    db_util.assemble_ql(pathlib.Path(default_common.param_main_db_cksql_file_path), pathlib.Path(default_path.output_db_all_in_one_cksql), cksql_meta, "sql")


def recreate() -> None:
    command = get_recreate_command(default_common.param_main_db_cksql_host,
                                   default_common.param_main_db_cksql_port,
                                   default_common.param_main_db_cksql_user,
                                   default_common.param_main_db_cksql_pass,
                                   default_common.param_main_db_name)
    logger.info(basic_util.action_formatter(__get_function_name(), command))
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
    return get_basic_param(default_common.param_main_db_cksql_host,
                           default_common.param_main_db_cksql_port,
                           default_common.param_main_db_cksql_user,
                           default_common.param_main_db_cksql_pass,
                           default_common.param_main_db_name)


def execute() -> None:
    extra_param_dict = [
        "--skip-column-names",
        "< " + default_path.output_db_all_in_one_cksql
    ]
    command = list_util.flat_to_str(cksql_cmd, get_main_db_param_dict(), extra_param_dict)
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command, db_util.print_ql_msg)


def get_recreate_command(host, port, user, password, db_name) -> str:
    extra_param_dict = [
        "--execute",
        "\"",
        "drop database if exists {0};".format(db_name),
        "create database if not exists {0} ENGINE = Atomic;".format(db_name),
        "\""
    ]
    return list_util.flat_to_str(cksql_cmd, get_basic_param(host, port, user, password, None), extra_param_dict)
