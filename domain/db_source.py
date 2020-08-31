# !/usr/bin/env python
import io
import math
import os
import re

from colorama import init, Fore

from script.domain import default_common as common
# from script.domain.db_meta import mysql as mysql_meta
from script.domain.db_meta import \
    mysql as mysql_meta, \
    neo4j as neo4j_meta
from script.utility import path, template

init(autoreset=True)


# assemble source sql files to target file
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


# regex filter item of list
def filter_execution(iterator):
    return list(filter(re.compile(r"^(executing:|executed:)").search, iterator))


def assemble_mysql():
    assemble_ql(common.param_main_db_mysql_file_path, common.param_main_db_mysql_output_file_name, mysql_meta, "sql")


# execute import sql file
def upgrade_mysql():
    command = recreate_mysql_command(common.param_main_db_host,
                                     common.param_main_db_mysql_port,
                                     common.param_main_db_mysql_user,
                                     common.param_main_db_mysql_pass,
                                     common.param_main_db_name) + \
              " && mysql" \
              " --default-character-set=utf8mb4" \
              " --database=" + common.param_main_db_name + \
              " --host=" + common.param_main_db_host + \
              " --port=" + common.param_main_db_mysql_port + \
              " --user=" + common.param_main_db_mysql_user + \
              " --password=" + common.param_main_db_mysql_pass + \
              " -N < " + common.param_main_db_mysql_output_file_name
    print(Fore.CYAN + upgrade_mysql.__name__ + " => " + Fore.WHITE + command)
    callback = filter_execution(os.popen(command).readlines())
    for m in callback[1::2]:
        print(Fore.GREEN + m.replace("\n", ""))
    if math.modf(len(callback) / 2)[0] > 0:
        print(Fore.RED + callback[len(callback) - 1])


# backup db
def backup_mysql():
    command = recreate_mysql_command(common.param_main_db_host,
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


def recreate_mysql_command(host, port, user, password, db_name):
    return "mysql" \
           " --default-character-set=utf8mb4" \
           " --host=" + host + \
           " --port=" + port + \
           " --user=" + user + \
           " --password=" + password + \
           " -e \"drop database if exists " + db_name + ";create database if not exists " + db_name + " default charset utf8mb4 collate utf8mb4_0900_ai_ci;\""


def recreate_neo4j_command(host, port, user, password, db_name):
    return "echo %PATH% "
    # return "cypher-shell" \
    #        " --address neo4j://" + host + ":" + port + \
    #        " --username " + user + \
    #        " --password " + password + \
    #        " --database " + db_name + " \"match(n) return n;\""


def recreate_neo4j():
    command = recreate_neo4j_command(common.param_main_db_host,
                                     common.param_main_db_neo4j_port,
                                     common.param_main_db_neo4j_user,
                                     common.param_main_db_neo4j_pass,
                                     "neo4j")
    print(Fore.CYAN + recreate_neo4j.__name__ + " => " + Fore.WHITE + command)
    os.system(command)


# recreate target db
def recreate_mysql():
    command = recreate_mysql_command(common.param_main_db_host,
                                     common.param_main_db_mysql_port,
                                     common.param_main_db_mysql_user,
                                     common.param_main_db_mysql_pass,
                                     common.param_main_db_name)
    print(Fore.CYAN + recreate_mysql.__name__ + " => " + Fore.WHITE + command)
    os.system(command)


def assemble_neo4j():
    assemble_ql(common.param_main_db_neo4j_file_path, common.param_main_db_neo4j_output_file_name, neo4j_meta, "cql")


def rebuild_mysql():
    assemble_mysql()
    upgrade_mysql()


def rebuild_neo4j():
    assemble_neo4j()
    recreate_neo4j()
