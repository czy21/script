#!/usr/bin/env python3
import logging
import pathlib

from utility import path as path_util

logger = logging.getLogger()

root_path = path_util.join_path(__file__, "../../../../")
output = path_util.join_path(root_path, "___output")
project_code = path_util.join_path(root_path, "code")
project_db = path_util.join_path(root_path, "db")

script_template = path_util.join_path(root_path, "script/template")

# child dir of code
project_code_api = path_util.join_path(project_code, "api")
project_code_web = path_util.join_path(project_code, "web")
project_code_app = path_util.join_path(project_code, "app")
project_code_plugin = path_util.join_path(project_code, "gradle-plugin")

# child dir of output
output_api = path_util.join_path(output, "api")
output_web = path_util.join_path(output, "web")
output_app = path_util.join_path(output, "app")
output_db = path_util.join_path(output, "db")
output_db_bak = path_util.join_path(output_db, "bak")
output_db_all_in_one = path_util.join_path(output_db, "all_in_one")

output_db_all_in_one_mysql = path_util.join_path(output_db_all_in_one, "mysql.sql")
output_db_all_in_one_pgsql = path_util.join_path(output_db_all_in_one, "pgsql.sql")
output_db_all_in_one_mssql = path_util.join_path(output_db_all_in_one, "mssql.sql")
output_db_all_in_one_chsql = path_util.join_path(output_db_all_in_one, "chsql.sql")
output_db_all_in_one_mongo = path_util.join_path(output_db_all_in_one, "mongo.mongo")
output_db_all_in_one_neo4j = path_util.join_path(output_db_all_in_one, "neo4j.neo4j")

output_db_bak_gz_mysql = path_util.join_path(output_db_bak, "mysql.gz")
output_db_bak_gz_pgsql = path_util.join_path(output_db_bak, "pgsql.gz")
output_db_bak_gz_mssql = path_util.join_path(output_db_bak, "mssql.gz")
output_db_bak_gz_mongo = path_util.join_path(output_db_bak, "mongo.gz")

output_db_bak_sql_mysql = path_util.join_path(output_db_bak, "mysql.sql")
output_db_bak_sql_pgsql = path_util.join_path(output_db_bak, "pgsql.sql")
output_db_bak_sql_mssql = path_util.join_path(output_db_bak, "mssql.sql")
output_db_bak_sql_mongo = path_util.join_path(output_db_bak, "mongo.sql")

output_tmp = path_util.join_path(output, "tmp")


def create_output() -> None:
    dirs = [output_tmp, output_api, output_web, output_app, output_db_bak, output_db_all_in_one]
    for p in dirs:
        pathlib.Path(p).mkdir(parents=True, exist_ok=True)
