#!/usr/bin/env python3
import os

from script.domain.default import common as default_common
from script.domain.default import path as default_path
from script.domain.db_meta import neo4j as neo4j_meta
from script.utility import db as db_util, collection as list_util, basic as basic_util, log

logger = log.Logger(__name__)


class Neo4j:
    @staticmethod
    def assemble() -> None:
        db_util.assemble_ql(default_common.param_main_db_neo4j_file_path, default_path.output_db_all_in_one_neo4j, neo4j_meta, "cql")

    @staticmethod
    def get_main_db_param_dict() -> list:
        return Neo4j.get_basic_param(default_common.param_main_db_host,
                                     default_common.param_main_db_neo4j_port,
                                     default_common.param_main_db_neo4j_user,
                                     default_common.param_main_db_neo4j_pass,
                                     default_common.param_main_db_name)

    @staticmethod
    def exec() -> None:
        extra_param_dict = [
            "--file " + default_path.output_db_all_in_one_neo4j
        ]
        basic_param_str = list_util.arr_param_to_str(Neo4j.get_main_db_param_dict(), extra_param_dict)
        command = "cypher-shell" + basic_param_str
        logger.info(basic_util.action_formatter("_".join([Neo4j.__name__, Neo4j.exec.__name__]), command))
        neo4j_msg = [elem.replace("\"", '') for elem in os.popen(command).readlines() if elem != "msg\n"]
        db_util.print_ql_msg(neo4j_msg)

    @staticmethod
    def get_basic_param(host, port, user, password, db_name) -> list:
        return [
            "--address " + "neo4j://" + host + ":" + port,
            "--username " + user,
            "--password " + password,
            "--database " + db_name
        ]

    @staticmethod
    def recreate() -> None:
        extra_param_dict = [
            "\"match(n) detach delete n;\""
        ]
        basic_param_str = list_util.arr_param_to_str(Neo4j.get_main_db_param_dict(), extra_param_dict)
        command = "cypher-shell" + basic_param_str
        logger.info(basic_util.action_formatter("_".join([Neo4j.__name__, Neo4j.recreate.__name__]), command))
        basic_util.execute(command)


def rebuild_neo4j():
    Neo4j.assemble()
    Neo4j.recreate()
    Neo4j.exec()
