# !/usr/bin/env python
import os

from script.domain import default_common as common
from script.domain.db_meta import mysql as mysql_meta, neo4j as neo4j_meta
from script.utility import db as db_util, list as list_util


class Mysql:
    @staticmethod
    def assemble():
        db_util.assemble_ql(common.param_main_db_mysql_file_path, common.param_main_db_mysql_output_file_name, mysql_meta, "sql", common)

    @staticmethod
    def recreate():
        command = Mysql.recreate_command(common.param_main_db_host,
                                         common.param_main_db_mysql_port,
                                         common.param_main_db_mysql_user,
                                         common.param_main_db_mysql_pass,
                                         common.param_main_db_name)
        db_util.print_cmd(Mysql.__name__, Mysql.recreate.__name__, command)
        os.system(command)

    @staticmethod
    def get_basic_param(host, port, user, password, db_name):
        return [
            "--default-character-set=utf8mb4",
            "--database=" + db_name,
            "--host=" + host,
            "--port=" + port,
            "--user=" + user,
            "--password=" + password
        ]

    @staticmethod
    def get_main_db_param_dict():
        return Mysql.get_basic_param(common.param_main_db_host,
                                     common.param_main_db_mysql_port,
                                     common.param_main_db_mysql_user,
                                     common.param_main_db_mysql_pass,
                                     common.param_main_db_name)

    @staticmethod
    def exec():
        extra_param_dict = [
            "--skip-column-names",
            "< " + common.param_main_db_mysql_output_file_name
        ]
        basic_param_str = list_util.arr_param_to_str(Mysql.get_main_db_param_dict(), extra_param_dict)
        command = "mysql" + basic_param_str
        db_util.print_cmd(Mysql.__name__, Mysql.exec.__name__, command)
        mysql_msg = os.popen(command).readlines()
        db_util.print_msg(mysql_msg)

    @staticmethod
    def recreate_command(host, port, user, password, db_name):
        extra_param_dict = [
            "--execute \"drop database if exists " + db_name + ";create database if not exists " + db_name + " default charset utf8mb4 collate utf8mb4_0900_ai_ci;\""
        ]
        basic_param_str = list_util.arr_param_to_str(Mysql.get_basic_param(host, port, user, password, db_name), extra_param_dict)
        return "mysql" + basic_param_str

    @staticmethod
    def backup_mysql():
        command = Mysql.recreate_command(common.param_main_db_host,
                                         common.param_main_db_mysql_port,
                                         common.param_main_db_mysql_user,
                                         common.param_main_db_mysql_pass,
                                         common.param_main_db_bak_name) + \
                  " && mysqldump" + list_util.arr_param_to_str(Mysql.get_basic_param(common.param_main_db_host,
                                                                                     common.param_main_db_mysql_port,
                                                                                     common.param_main_db_mysql_user,
                                                                                     common.param_main_db_mysql_pass,
                                                                                     common.param_main_db_name)) + \
                  "| mysql" + list_util.arr_param_to_str(Mysql.get_basic_param(common.param_main_db_host,
                                                                               common.param_main_db_mysql_port,
                                                                               common.param_main_db_mysql_user,
                                                                               common.param_main_db_mysql_pass,
                                                                               common.param_main_db_bak_name))
        # print(Fore.CYAN + "restoring => " + Fore.WHITE + command)
        os.system(command)


class Neo4j:
    @staticmethod
    def assemble():
        db_util.assemble_ql(common.param_main_db_neo4j_file_path, common.param_main_db_neo4j_output_file_name, neo4j_meta, "cql", common)

    @staticmethod
    def get_main_db_param_dict():
        return Neo4j.get_basic_param(common.param_main_db_host,
                                     common.param_main_db_neo4j_port,
                                     common.param_main_db_neo4j_user,
                                     common.param_main_db_neo4j_pass,
                                     common.param_main_db_neo4j_db_name)

    @staticmethod
    def exec():
        extra_param_dict = [
            "--file " + common.param_main_db_neo4j_output_file_name
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


def rebuild_mysql():
    Mysql.assemble()
    Mysql.recreate()
    Mysql.exec()


def rebuild_neo4j():
    Neo4j.assemble()
    Neo4j.recreate()
    Neo4j.exec()
