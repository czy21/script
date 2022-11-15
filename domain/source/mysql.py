#!/usr/bin/env python3
import logging
import pathlib

from domain.db_meta import mysql as mysql_meta
from domain.default import common as default_common
from domain.default import path as default_path
from utility import db as db_util, collection as list_util, basic as basic_util

logger = logging.getLogger()

mysql_cmd = "mysql"


def assemble() -> None:
    db_util.assemble_ql(pathlib.Path(default_common.param_main_db_mysql_file_path), pathlib.Path(default_path.output_db_all_in_one_mysql), mysql_meta, "sql")


def recreate() -> None:
    command = get_recreate_command(default_common.param_main_db_mysql_host,
                                   default_common.param_main_db_mysql_port,
                                   default_common.param_main_db_mysql_user,
                                   default_common.param_main_db_mysql_pass,
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
    return get_basic_param(default_common.param_main_db_mysql_host,
                           default_common.param_main_db_mysql_port,
                           default_common.param_main_db_mysql_user,
                           default_common.param_main_db_mysql_pass,
                           default_common.param_main_db_name)


def execute() -> None:
    extra_param_dict = [
        "--skip-column-names",
        "< " + default_path.output_db_all_in_one_mysql
    ]
    command = list_util.flat_to_str([mysql_cmd, get_main_db_param_dict(), extra_param_dict])
    basic_util.execute(command, db_util.print_ql_msg)


def get_recreate_command(host, port, user, password, db_name) -> str:
    extra_param = [
        "--execute \"{0}\"".format("".join(
            [
                "drop database if exists {0};".format(db_name),
                "create database if not exists {0} default charset utf8mb4 collate utf8mb4_unicode_ci;".format(db_name),
            ])
        )
    ]
    return list_util.flat_to_str([mysql_cmd, get_basic_param(host, port, user, password, None), extra_param])


def backup_db() -> None:
    recreate_command = get_recreate_command(default_common.param_main_db_mysql_host,
                                            default_common.param_main_db_mysql_port,
                                            default_common.param_main_db_mysql_user,
                                            default_common.param_main_db_mysql_pass,
                                            default_common.param_main_db_bak_name)
    command = list_util.flat_to_str(recreate_command,
                                    "&&mysqldump",
                                    list_util.flat_to_str([
                                        get_basic_param(default_common.param_main_db_mysql_host,
                                                        default_common.param_main_db_mysql_port,
                                                        default_common.param_main_db_mysql_user,
                                                        default_common.param_main_db_mysql_pass, None),
                                        "--opt",
                                        default_common.param_main_db_name,
                                        "--max-allowed-packet=1024M"
                                    ]),
                                    "| mysql",
                                    list_util.flat_to_str([
                                        get_basic_param(default_common.param_main_db_mysql_host,
                                                        default_common.param_main_db_mysql_port,
                                                        default_common.param_main_db_mysql_user,
                                                        default_common.param_main_db_mysql_pass,
                                                        None),
                                        "--compress",
                                        default_common.param_main_db_bak_name,
                                    ]))
    basic_util.execute(command)


def backup_sql() -> None:
    command = list_util.flat_to_str("mysqldump",
                                    list_util.flat_to_str([
                                        get_basic_param(default_common.param_main_db_mysql_host,
                                                        default_common.param_main_db_mysql_port,
                                                        default_common.param_main_db_mysql_user,
                                                        default_common.param_main_db_mysql_pass, None),
                                        "--opt",
                                        default_common.param_main_db_name,
                                    ]),
                                    "--skip-opt",
                                    "--complete-insert",
                                    " > ",
                                    default_path.output_db_bak_sql_mysql
                                    )
    basic_util.execute(command)


def backup_gz() -> None:
    command = list_util.flat_to_str("mysqldump",
                                    list_util.flat_to_str([
                                        get_basic_param(default_common.param_main_db_mysql_host,
                                                        default_common.param_main_db_mysql_port,
                                                        default_common.param_main_db_mysql_user,
                                                        default_common.param_main_db_mysql_pass, None),
                                        "--opt",
                                        default_common.param_main_db_name,
                                    ]),
                                    "| gzip > ",
                                    default_path.output_db_bak_gz_mysql
                                    )
    basic_util.execute(command)


def restore_gz() -> None:
    recreate_command = get_recreate_command(default_common.param_main_db_mysql_host,
                                            default_common.param_main_db_mysql_port,
                                            default_common.param_main_db_mysql_user,
                                            default_common.param_main_db_mysql_pass,
                                            default_common.param_main_db_name)
    command = list_util.flat_to_str(recreate_command,
                                    "&& gzip -d < ",
                                    default_path.output_db_bak_gz_mysql,
                                    "| mysql",
                                    list_util.flat_to_str([
                                        get_basic_param(default_common.param_main_db_mysql_host,
                                                        default_common.param_main_db_mysql_port,
                                                        default_common.param_main_db_mysql_user,
                                                        default_common.param_main_db_mysql_pass,
                                                        default_common.param_main_db_name)
                                    ]))
    basic_util.execute(command)
