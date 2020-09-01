#!/usr/bin/env python3
import os

from script.domain.default import common as default_common
from script.domain.db_meta import neo4j as neo4j_meta
from script.utility import db as db_util, list as list_util


class Neo4j:
    @staticmethod
    def assemble():
        db_util.assemble_ql(default_common.param_main_db_neo4j_file_path, default_common.param_main_db_neo4j_output_file_name, neo4j_meta, "cql")

    @staticmethod
    def get_main_db_param_dict():
        return Neo4j.get_basic_param(default_common.param_main_db_host,
                                     default_common.param_main_db_neo4j_port,
                                     default_common.param_main_db_neo4j_user,
                                     default_common.param_main_db_neo4j_pass,
                                     default_common.param_main_db_neo4j_db_name)

    @staticmethod
    def exec():
        extra_param_dict = [
            "--file " + default_common.param_main_db_neo4j_output_file_name
        ]
        basic_param_str = list_util.arr_param_to_str(Neo4j.get_main_db_param_dict(), extra_param_dict)
        command = "cypher-shell" + basic_param_str
        db_util.print_cmd(Neo4j.__name__, Neo4j.exec.__name__, command)
        neo4j_msg = [elem.replace("\"", '') for elem in os.popen(command).readlines() if elem != "msg\n"]
        db_util.print_msg(neo4j_msg)

    @staticmethod
    def get_basic_param(host, port, user, password, db_name):
        return [
            "--address " + "neo4j://" + host + ":" + port,
            "--username " + user,
            "--password " + password,
            "--database " + db_name
        ]

    @staticmethod
    def recreate():
        extra_param_dict = [
            "\"match(n) detach delete n;\""
        ]
        basic_param_str = list_util.arr_param_to_str(Neo4j.get_main_db_param_dict(), extra_param_dict)
        command = "cypher-shell" + basic_param_str
        db_util.print_cmd(Neo4j.__name__, Neo4j.recreate.__name__, command)
        os.system(command)


def rebuild_neo4j():
    Neo4j.assemble()
    Neo4j.recreate()
    Neo4j.exec()
