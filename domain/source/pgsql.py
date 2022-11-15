#!/usr/bin/env python3
import logging
import os
import pathlib

from domain.db_meta import pgsql as pgsql_meta
from domain.default import common as default_common
from domain.default import path as default_path
from utility import db as db_util, collection as list_util, basic as basic_util

logger = logging.getLogger()

psql_cmd = "psql"
pg_dump_cmd = "pg_dump"


def assemble() -> None:
    db_util.assemble_ql(pathlib.Path(default_common.param_main_db_pgsql_file_path), pathlib.Path(default_path.output_db_all_in_one_pgsql), pgsql_meta, "sql")


def recreate() -> None:
    command = get_recreate_command(default_common.param_main_db_pgsql_host,
                                   default_common.param_main_db_pgsql_port,
                                   default_common.param_main_db_pgsql_user,
                                   default_common.param_main_db_pgsql_pass,
                                   default_common.param_main_db_name)
    basic_util.execute(command)


def get_basic_param(host, port, user, password, db_name) -> str:
    param = ["--host=" + host,
             "--port=" + port,
             "--username=" + user
             ]
    if db_name:
        param.append("--dbname=" + db_name)
    return list_util.flat_to_str(param)


def get_main_db_param_dict() -> str:
    return get_basic_param(default_common.param_main_db_pgsql_host,
                           default_common.param_main_db_pgsql_port,
                           default_common.param_main_db_pgsql_user,
                           default_common.param_main_db_pgsql_pass,
                           default_common.param_main_db_name)


def execute() -> None:
    command = list_util.flat_to_str(
        "PGPASSWORD=" + default_common.param_main_db_pgsql_pass,
        psql_cmd,
        get_main_db_param_dict(),
        "< " + default_path.output_db_all_in_one_pgsql
    )
    basic_util.execute(command, db_util.print_ql_msg, encoding="gbk" if os.name == 'nt' else "utf-8")


def get_recreate_command(host, port, user, password, db_name) -> str:
    cmd = [
        "echo \"{0}\"".format("".join(
            [
                "drop database if exists {0} WITH (FORCE);".format(db_name),
                "CREATE DATABASE {} WITH OWNER = postgres ENCODING = \'UTF8\' CONNECTION LIMIT = -1;".format(db_name)
            ])
        ),
        "|",
        "PGPASSWORD=" + default_common.param_main_db_pgsql_pass,
        psql_cmd,
        get_basic_param(host, port, user, password, None)
    ]
    return list_util.flat_to_str(cmd)


def backup_gz() -> None:
    cmd = list_util.flat_to_str([
        "PGPASSWORD=" + default_common.param_main_db_pgsql_pass,
        pg_dump_cmd,
        get_main_db_param_dict(),
        "--column-inserts",
        "| gzip > ",
        default_path.output_db_bak_gz_pgsql
    ])
    basic_util.execute(cmd)


def backup_sql() -> None:
    cmd = list_util.flat_to_str([
        "PGPASSWORD=" + default_common.param_main_db_pgsql_pass,
        pg_dump_cmd,
        get_main_db_param_dict(),
        "--column-inserts",
        "--file=" + default_path.output_db_bak_sql_pgsql
    ])
    basic_util.execute(cmd)
