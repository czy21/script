# !/usr/bin/env python
import io
import math
import os
import re

from colorama import init, Fore

from script.domain import default_common as common
from script.domain.db_meta import mysql as mysql_meta, neo4j as neo4j_meta
from script.utility import path, template

init(autoreset=True)


def assemble_ql(s_path, t_file_name, db_meta, file_suffix):
    db_file_paths = path.dfs_dir(s_path, re.compile(r".*" + file_suffix))
    with io.open(t_file_name, "w+", encoding="utf-8", newline="\n") as t_file:
        for s in db_file_paths:
            header = template.StringTemplate(db_meta.self["header"])
            footer = template.StringTemplate(db_meta.self["footer"])
            print(Fore.GREEN + "loading => " + Fore.WHITE + s)
            t_file.write(u'{}'.format(header.safe_substitute(file_path=s) + "\n"))
            with io.open(s, "r", encoding="utf-8", newline="\n") as current_sql_file:
                t_file.write(
                    template.StringTemplate(current_sql_file.read() + "\n")
                        .safe_substitute(dict(db_meta.self["substitution"], **common.get_params())))
            t_file.write(u'{}'.format(footer.safe_substitute(file_path=s) + "\n\n"))


def filter_execution(iterator):
    return list(filter(re.compile(r"^(executing:|executed:)").search, iterator))


def print_msg(msg_lines):
    callback = filter_execution(msg_lines)
    for m in callback[1::2]:
        print(Fore.GREEN + m.replace("\n", ""))
    if math.modf(len(callback) / 2)[0] > 0:
        print(Fore.RED + callback[len(callback) - 1])


def print_cmd(class_name, method_name, command):
    print(Fore.CYAN + class_name + "_" + method_name + " => " + Fore.WHITE + command)


class Mysql:
    @staticmethod
    def assemble():
        assemble_ql(common.param_main_db_mysql_file_path, common.param_main_db_mysql_output_file_name, mysql_meta, "sql")

    @staticmethod
    def recreate():
        command = Mysql.recreate_command(common.param_main_db_host,
                                         common.param_main_db_mysql_port,
                                         common.param_main_db_mysql_user,
                                         common.param_main_db_mysql_pass,
                                         common.param_main_db_name)
        print_cmd(Mysql.__name__, Mysql.recreate.__name__, command)
        os.system(command)

    @staticmethod
    def exec():
        command = " mysql" \
                  " --default-character-set=utf8mb4" \
                  " --database=" + common.param_main_db_name + \
                  " --host=" + common.param_main_db_host + \
                  " --port=" + common.param_main_db_mysql_port + \
                  " --user=" + common.param_main_db_mysql_user + \
                  " --password=" + common.param_main_db_mysql_pass + \
                  " -N < " + common.param_main_db_mysql_output_file_name
        print_cmd(Mysql.__name__, Mysql.exec.__name__, command)
        mysql_msg = os.popen(command).readlines()
        print_msg(mysql_msg)

    @staticmethod
    def recreate_command(host, port, user, password, db_name):
        return "mysql" \
               " --default-character-set=utf8mb4" \
               " --host=" + host + \
               " --port=" + port + \
               " --user=" + user + \
               " --password=" + password + \
               " -e \"drop database if exists " + db_name + ";create database if not exists " + db_name + " default charset utf8mb4 collate utf8mb4_0900_ai_ci;\""

    @staticmethod
    def backup_mysql():
        command = Mysql.recreate_command(common.param_main_db_host,
                                         common.param_main_db_mysql_port,
                                         common.param_main_db_mysql_user,
                                         common.param_main_db_mysql_pass,
                                         common.param_main_db_bak_name) + \
                  " && mysqldump " + common.param_main_db_name + \
                  " --default-character-set=utf8mb4" \
                  " --host=" + common.param_main_db_host + \
                  " --port=" + common.param_main_db_mysql_port + \
                  " --user=" + common.param_main_db_mysql_user + \
                  " --password=" + common.param_main_db_mysql_pass + \
                  "| mysql " \
                  " --default-character-set=utf8mb4" \
                  " --database=" + common.param_main_db_bak_name + \
                  " --host=" + common.param_main_db_host + \
                  " --port=" + common.param_main_db_mysql_port + \
                  " --user=" + common.param_main_db_mysql_user + \
                  " --password=" + common.param_main_db_mysql_pass
        print(Fore.CYAN + "restoring => " + Fore.WHITE + command)
        os.system(command)


class Neo4j:
    @staticmethod
    def assemble():
        assemble_ql(common.param_main_db_neo4j_file_path, common.param_main_db_neo4j_output_file_name, neo4j_meta, "cql")

    @staticmethod
    def exec():
        command = "cypher-shell" \
                  " --address neo4j://" + common.param_main_db_host + ":" + common.param_main_db_neo4j_port + \
                  " --username " + common.param_main_db_neo4j_user + \
                  " --password " + common.param_main_db_neo4j_pass + \
                  " --database " + common.param_main_db_neo4j_db_name + \
                  " --file " + common.param_main_db_neo4j_output_file_name
        print_cmd(Neo4j.__name__, Neo4j.exec.__name__, command)
        neo4j_msg = [elem.replace("\"", '') for elem in os.popen(command).readlines() if elem != "msg\n"]
        print_msg(neo4j_msg)

    @staticmethod
    def recreate():
        command = "cypher-shell" \
                  " --address neo4j://" + common.param_main_db_host + ":" + common.param_main_db_neo4j_port + \
                  " --username " + common.param_main_db_neo4j_user + \
                  " --password " + common.param_main_db_neo4j_pass + \
                  " --database " + common.param_main_db_neo4j_db_name + " \"match(n) detach delete n;\""
        print_cmd(Neo4j.__name__, Neo4j.recreate.__name__, command)
        os.system(command)


def rebuild_mysql():
    Mysql.assemble()
    Mysql.recreate()
    Mysql.exec()


def rebuild_neo4j():
    Neo4j.assemble()
    Neo4j.recreate()
    Neo4j.exec()
