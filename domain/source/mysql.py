#!/usr/bin/env python3
import inspect

from script.domain.db_meta import mysql as mysql_meta
from script.domain.default import common as default_common
from script.domain.default import path as default_path
from script.utility import db as db_util, collection as list_util, basic as basic_util, log

logger = log.Logger(__name__)


def __get_function_name():
    return inspect.stack()[1][3]


def assemble() -> None:
    db_util.assemble_ql(default_common.param_main_db_mysql_file_path, default_path.output_db_all_in_one_mysql, mysql_meta, "sql")


def recreate() -> None:
    command = recreate_command(default_common.param_main_db_mysql_host,
                               default_common.param_main_db_mysql_port,
                               default_common.param_main_db_mysql_user,
                               default_common.param_main_db_mysql_pass,
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
    return list_util.arr_param_to_str(param)


def get_main_db_param_dict() -> str:
    return get_basic_param(default_common.param_main_db_mysql_host,
                           default_common.param_main_db_mysql_port,
                           default_common.param_main_db_mysql_user,
                           default_common.param_main_db_mysql_pass,
                           default_common.param_main_db_name)


def exec() -> None:
    extra_param_dict = [
        "--skip-column-names",
        "< " + default_path.output_db_all_in_one_mysql
    ]
    command = list_util.arr_param_to_str("mysql", get_main_db_param_dict(), extra_param_dict)
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command, db_util.print_ql_msg)


def recreate_command(host, port, user, password, db_name) -> str:
    extra_param_dict = [
        "--execute",
        "\"",
        "drop database if exists {0};".format(db_name),
        "create database if not exists {0} default charset utf8mb4 collate utf8mb4_0900_ai_ci;".format(db_name),
        "\""
    ]
    return list_util.arr_param_to_str("mysql", get_basic_param(host, port, user, password, None), extra_param_dict)


def backup_mysql() -> None:
    command = list_util.arr_param_to_str(recreate_command(default_common.param_main_db_mysql_host,
                                                          default_common.param_main_db_mysql_port,
                                                          default_common.param_main_db_mysql_user,
                                                          default_common.param_main_db_mysql_pass,
                                                          default_common.param_main_db_bak_name),
                                         "&&mysqldump",
                                         get_basic_param(default_common.param_main_db_mysql_host,
                                                         default_common.param_main_db_mysql_port,
                                                         default_common.param_main_db_mysql_user,
                                                         default_common.param_main_db_mysql_pass,
                                                         default_common.param_main_db_name),
                                         "|mysql",
                                         get_basic_param(default_common.param_main_db_mysql_host,
                                                         default_common.param_main_db_mysql_port,
                                                         default_common.param_main_db_mysql_user,
                                                         default_common.param_main_db_mysql_pass,
                                                         default_common.param_main_db_bak_name)
                                         )
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)
