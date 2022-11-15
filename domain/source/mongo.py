#!/usr/bin/env python3
import logging
import pathlib

from domain.db_meta import mongo as mongo_meta
from domain.default import common as default_common
from domain.default import path as default_path
from utility import db as db_util, collection as list_util, basic as basic_util

logger = logging.getLogger()


def assemble() -> None:
    db_util.assemble_ql(pathlib.Path(default_common.param_main_db_mongo_file_path), pathlib.Path(default_path.output_db_all_in_one_mongo), mongo_meta, "mongo")


def recreate() -> None:
    command = get_recreate_command(default_common.param_main_db_mongo_host,
                                   default_common.param_main_db_mongo_port,
                                   default_common.param_main_db_mongo_user,
                                   default_common.param_main_db_mongo_pass,
                                   default_common.param_main_db_name)
    basic_util.execute(command)


def get_basic_uri(host, port, user, password, db_name) -> str:
    return "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(user, password, host, port, db_name if db_name is not None else "")


def get_main_db_uri() -> str:
    return get_basic_uri(default_common.param_main_db_mongo_host,
                         default_common.param_main_db_mongo_port,
                         default_common.param_main_db_mongo_user,
                         default_common.param_main_db_mongo_pass,
                         default_common.param_main_db_name)


def execute() -> None:
    extra_param = [
        default_path.output_db_all_in_one_mongo
    ]
    command = list_util.flat_to_str("mongo", get_main_db_uri(), extra_param)
    basic_util.execute(command, db_util.print_ql_msg)


def get_recreate_command(host, port, user, password, db_name) -> str:
    extra_param = [
        "--eval \"{0}\"".format("".join(
            [
                "db = db.getSiblingDB('{0}');db.dropDatabase();".format(db_name)
            ])
        )
    ]
    return list_util.flat_to_str("mongo", get_basic_uri(host, port, user, password, None), extra_param)


def backup_gz() -> None:
    command = list_util.flat_to_str("mongodump",
                                    "--uri=" + get_main_db_uri(),
                                    "--archive=" + default_path.output_db_bak_gz_mongo,
                                    "--gzip"
                                    )
    basic_util.execute(command)
