#!/usr/bin/env python3
import inspect

from script.domain.db_meta import mongo as mongo_meta
from script.domain.default import common as default_common
from script.domain.default import path as default_path
from script.utility import db as db_util, collection as list_util, basic as basic_util, log

logger = log.Logger(__name__)


def __get_function_name():
    return inspect.stack()[1][3]


def assemble() -> None:
    db_util.assemble_ql(default_common.param_main_db_mongo_file_path, default_path.output_db_all_in_one_mongo, mongo_meta, "mongo")


def recreate() -> None:
    command = get_recreate_command(default_common.param_main_db_mongo_host,
                                   default_common.param_main_db_mongo_port,
                                   default_common.param_main_db_mongo_user,
                                   default_common.param_main_db_mongo_pass,
                                   default_common.param_main_db_name)
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)


def get_basic_param(host, port, user, password, db_name) -> str:
    param = ["--host " + host,
             "--port " + port,
             "--username " + user,
             "--password " + password,
             ]
    if db_name:
        param.append(db_name)
    param.append("--authenticationDatabase admin")
    return list_util.arr_param_to_str(param)


def get_main_db_param_dict() -> str:
    return get_basic_param(default_common.param_main_db_mongo_host,
                           default_common.param_main_db_mongo_port,
                           default_common.param_main_db_mongo_user,
                           default_common.param_main_db_mongo_pass,
                           default_common.param_main_db_name)


def exec() -> None:
    extra_param_dict = [
        default_path.output_db_all_in_one_mongo
    ]
    command = list_util.arr_param_to_str("mongo", get_main_db_param_dict(), extra_param_dict)
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command, db_util.print_ql_msg)


def get_recreate_command(host, port, user, password, db_name) -> str:
    extra_param_dict = [
        "--execute",
        "\"",
        "drop database if exists {0};".format(db_name),
        "create database if not exists {0} default charset utf8mb4 collate utf8mb4_0900_ai_ci;".format(db_name),
        "\""
    ]
    return list_util.arr_param_to_str("mysql", get_basic_param(host, port, user, password, None), extra_param_dict)


def backup_db() -> None:
    command = list_util.arr_param_to_str(get_recreate_command(default_common.param_main_db_mongo_host,
                                                              default_common.param_main_db_mongo_port,
                                                              default_common.param_main_db_mongo_user,
                                                              default_common.param_main_db_mongo_pass,
                                                              default_common.param_main_db_bak_name),
                                         "&&mysqldump",
                                         list_util.arr_param_to_str([
                                             get_basic_param(default_common.param_main_db_mongo_host,
                                                             default_common.param_main_db_mongo_port,
                                                             default_common.param_main_db_mongo_user,
                                                             default_common.param_main_db_mongo_pass, None),
                                             "--opt",
                                             default_common.param_main_db_name,
                                             "--max-allowed-packet=1024M"
                                         ]),
                                         "| mysql",
                                         list_util.arr_param_to_str([
                                             get_basic_param(default_common.param_main_db_mongo_host,
                                                             default_common.param_main_db_mongo_port,
                                                             default_common.param_main_db_mongo_user,
                                                             default_common.param_main_db_mongo_pass,
                                                             None),
                                             "--compress",
                                             default_common.param_main_db_bak_name,
                                         ]))
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)


def backup_gz() -> None:
    command = list_util.arr_param_to_str("mongodump",
                                         "--uri=" + "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(default_common.param_main_db_mongo_user,
                                                                                                       default_common.param_main_db_mongo_pass,
                                                                                                       default_common.param_main_db_mongo_host,
                                                                                                       default_common.param_main_db_mongo_port,
                                                                                                       default_common.param_main_db_name),
                                         "--archive=" + default_path.output_db_bak_gz_mongo,
                                         "--gzip"
                                         )
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)


def restore_gz() -> None:
    recreate_command = get_recreate_command(default_common.param_main_db_mongo_host,
                                            default_common.param_main_db_mongo_port,
                                            default_common.param_main_db_mongo_user,
                                            default_common.param_main_db_mongo_pass,
                                            default_common.param_main_db_name)
    command = list_util.arr_param_to_str(recreate_command,
                                         "&& gzip -d < ",
                                         default_path.output_db_bak_gz_mongo,
                                         "| mysql",
                                         list_util.arr_param_to_str([
                                             get_basic_param(default_common.param_main_db_mongo_host,
                                                             default_common.param_main_db_mongo_port,
                                                             default_common.param_main_db_mongo_user,
                                                             default_common.param_main_db_mongo_pass,
                                                             default_common.param_main_db_name)
                                         ]))
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)
