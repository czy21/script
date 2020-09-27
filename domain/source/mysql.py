#!/usr/bin/env python3
import os

from script.domain.db_meta import mysql as mysql_meta
from script.domain.default import common as default_common
from script.utility import db as db_util, list as list_util


class Mysql:
    @staticmethod
    def assemble() -> None:
        db_util.assemble_ql(default_common.param_main_db_mysql_file_path, default_common.param_main_db_mysql_output_file_name, mysql_meta, "sql")

    @staticmethod
    def recreate() -> None:
        command = Mysql.recreate_command(default_common.param_main_db_host,
                                         default_common.param_main_db_mysql_port,
                                         default_common.param_main_db_mysql_user,
                                         default_common.param_main_db_mysql_pass,
                                         default_common.param_main_db_name)
        db_util.print_cmd(Mysql.__name__, Mysql.recreate.__name__, command)
        os.system(command)

    @staticmethod
    def get_basic_param(host, port, user, password, db_name) -> str:
        param = ["--default-character-set=utf8mb4",
                 "--host=" + host,
                 "--port=" + port,
                 "--user=" + user,
                 "--password=" + password
                 ]
        if db_name:
            param.append("--database=" + db_name)
        return list_util.arr_param_to_str(param)

    @staticmethod
    def get_main_db_param_dict() -> str:
        return Mysql.get_basic_param(default_common.param_main_db_host,
                                     default_common.param_main_db_mysql_port,
                                     default_common.param_main_db_mysql_user,
                                     default_common.param_main_db_mysql_pass,
                                     default_common.param_main_db_name)

    @staticmethod
    def exec() -> None:
        extra_param_dict = [
            "--skip-column-names",
            "< " + default_common.param_main_db_mysql_output_file_name
        ]
        command = list_util.arr_param_to_str("mysql", Mysql.get_main_db_param_dict(), extra_param_dict)
        db_util.print_cmd(Mysql.__name__, Mysql.exec.__name__, command)
        mysql_msg = os.popen(command).readlines()
        db_util.print_msg(mysql_msg)

    @staticmethod
    def recreate_command(host, port, user, password, db_name) -> str:
        extra_param_dict = [
            "--execute \"drop database if exists " + db_name + ";create database if not exists " + db_name + " default charset utf8mb4 collate utf8mb4_0900_ai_ci;\""
        ]
        return list_util.arr_param_to_str("mysql", Mysql.get_basic_param(host, port, user, password, None), extra_param_dict)

    @staticmethod
    def backup_mysql() -> None:
        command = list_util.arr_param_to_str(Mysql.recreate_command(default_common.param_main_db_host,
                                                                    default_common.param_main_db_mysql_port,
                                                                    default_common.param_main_db_mysql_user,
                                                                    default_common.param_main_db_mysql_pass,
                                                                    default_common.param_main_db_bak_name),
                                             "&&mysqldump",
                                             Mysql.get_basic_param(default_common.param_main_db_host,
                                                                   default_common.param_main_db_mysql_port,
                                                                   default_common.param_main_db_mysql_user,
                                                                   default_common.param_main_db_mysql_pass,
                                                                   default_common.param_main_db_name),
                                             "|mysql",
                                             Mysql.get_basic_param(default_common.param_main_db_host,
                                                                   default_common.param_main_db_mysql_port,
                                                                   default_common.param_main_db_mysql_user,
                                                                   default_common.param_main_db_mysql_pass,
                                                                   default_common.param_main_db_bak_name)
                                             )
        db_util.print_cmd(Mysql.__name__, Mysql.backup_mysql.__name__, command)
        # os.system(command)


def rebuild_mysql():
    Mysql.assemble()
    Mysql.recreate()
    Mysql.exec()
