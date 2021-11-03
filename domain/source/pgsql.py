#!/usr/bin/env python3
import inspect

from script.domain.db_meta import pgsql as pgsql_meta
from script.domain.default import common as default_common
from script.domain.default import path as default_path
from script.utility import db as db_util, collection as list_util, basic as basic_util, log

logger = log.Logger(__name__)

pgsql_cmd = "psql"


def __get_function_name():
    return inspect.stack()[1][3]


def assemble() -> None:
    db_util.assemble_ql(default_common.param_main_db_pgsql_file_path, default_path.output_db_all_in_one_pgsql, pgsql_meta, "sql")


def recreate() -> None:
    command = get_recreate_command(default_common.param_main_db_pgsql_host,
                                   default_common.param_main_db_pgsql_port,
                                   default_common.param_main_db_pgsql_user,
                                   default_common.param_main_db_pgsql_pass,
                                   default_common.param_main_db_name)
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)


def get_basic_param(host, port, user, password, db_name) -> str:
    url = "postgresql://{}:{}@{}:{}".format(user, password, host, port)
    if db_name:
        url = url + "/" + db_name
    return "\"" + url + "\""


def get_main_db_param_dict() -> str:
    return get_basic_param(default_common.param_main_db_pgsql_host,
                           default_common.param_main_db_pgsql_port,
                           default_common.param_main_db_pgsql_user,
                           default_common.param_main_db_pgsql_pass,
                           default_common.param_main_db_name)


def execute() -> None:
    extra_param_dict = [
        "< " + default_path.output_db_all_in_one_pgsql
    ]
    command = list_util.arr_param_to_str(pgsql_cmd, get_main_db_param_dict(), extra_param_dict)
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command, db_util.print_ql_msg)


def get_recreate_command(host, port, user, password, db_name) -> str:
    cmd = [
        "echo",
        [
            "drop database if exists {0} WITH (FORCE);".format(db_name),
            "CREATE DATABASE {} WITH OWNER = postgres ENCODING = 'UTF8' CONNECTION LIMIT = -1;".format(db_name)
        ],
        "|",
        pgsql_cmd,
        get_basic_param(host, port, user, password, None)
    ]
    return list_util.arr_param_to_str(cmd)

def backup_gz() -> None:
    basic_util.execute("PGPASSWORD=***REMOVED*** pg_dump --dbname=erp_local --host=192.168.2.25 --port=5432 --username=postgres --column-inserts --file duml.sql")