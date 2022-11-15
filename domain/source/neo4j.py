#!/usr/bin/env python3
import logging
import os
import pathlib

from domain.db_meta import neo4j as neo4j_meta
from domain.default import common as default_common
from domain.default import path as default_path
from utility import db as db_util, collection as list_util, basic as basic_util, log

logger = logging.getLogger()


def assemble() -> None:
    db_util.assemble_ql(pathlib.Path(default_common.param_main_db_neo4j_file_path), pathlib.Path(default_path.output_db_all_in_one_neo4j), neo4j_meta, "cql")


def get_main_db_param_dict() -> list:
    return get_basic_param(default_common.param_main_db_neo4j_host,
                           default_common.param_main_db_neo4j_port,
                           default_common.param_main_db_neo4j_user,
                           default_common.param_main_db_neo4j_pass,
                           default_common.param_main_db_name)


def exec() -> None:
    extra_param_dict = [
        "--file " + default_path.output_db_all_in_one_neo4j
    ]
    basic_param_str = list_util.flat_to_str(get_main_db_param_dict(), extra_param_dict)
    command = "cypher-shell" + basic_param_str
    neo4j_msg = [elem.replace("\"", '') for elem in os.popen(command).readlines() if elem != "msg\n"]
    db_util.print_ql_msg(neo4j_msg)


def get_basic_param(host, port, user, password, db_name) -> list:
    return [
        "--address " + "neo4j://" + host + ":" + port,
        "--username " + user,
        "--password " + password,
        "--database " + db_name
    ]


def recreate() -> None:
    extra_param_dict = [
        "\"match(n) detach delete n;\""
    ]
    basic_param_str = list_util.flat_to_str(get_main_db_param_dict(), extra_param_dict)
    command = "cypher-shell" + basic_param_str
    basic_util.execute(command)
