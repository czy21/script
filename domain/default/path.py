#!/usr/bin/env python3
import shutil
from pathlib import Path

from script.utility import log, basic as basic_util
from script.utility import path as path_util

logger = log.Logger(__name__)

root_path = path_util.pure_path_join(__file__, "../../../../")
output = path_util.pure_path_join(root_path, "___output")
project_code = path_util.pure_path_join(root_path, "code")
project_db = path_util.pure_path_join(root_path, "db")

script_template = path_util.pure_path_join(root_path, "script/template")

# child dir of code
project_code_api = path_util.pure_path_join(project_code, "api")
project_code_web = path_util.pure_path_join(project_code, "web")
project_code_app = path_util.pure_path_join(project_code, "app")
project_plugin = path_util.pure_path_join(project_code, "gradle-plugin")

# child dir of output
output_api = path_util.pure_path_join(output, "api")
output_web = path_util.pure_path_join(output, "web")
output_app = path_util.pure_path_join(output, "app")
output_db = path_util.pure_path_join(output, "db")
output_db_bak = path_util.pure_path_join(output_db, "bak")
output_db_all_in_one = path_util.pure_path_join(output_db, "all_in_one")

output_db_all_in_one_mysql = path_util.pure_path_join(output_db_all_in_one, "mysql.sql")
output_db_all_in_one_pgsql = path_util.pure_path_join(output_db_all_in_one, "pgsql.sql")
output_db_all_in_one_mssql = path_util.pure_path_join(output_db_all_in_one, "mssql.sql")
output_db_all_in_one_cksql = path_util.pure_path_join(output_db_all_in_one, "cksql.sql")
output_db_all_in_one_mongo = path_util.pure_path_join(output_db_all_in_one, "mongo.mongo")
output_db_all_in_one_neo4j = path_util.pure_path_join(output_db_all_in_one, "neo4j.neo4j")

output_db_bak_gz_mysql = path_util.pure_path_join(output_db_bak, "mysql.gz")
output_db_bak_gz_pgsql = path_util.pure_path_join(output_db_bak, "pgsql.gz")
output_db_bak_gz_mongo = path_util.pure_path_join(output_db_bak, "mongo.gz")

output_db_bak_sql_mysql = path_util.pure_path_join(output_db_bak, "mysql.sql")
output_db_bak_sql_pgsql = path_util.pure_path_join(output_db_bak, "pgsql.sql")
output_db_bak_sql_mongo = path_util.pure_path_join(output_db_bak, "mongo.sql")

output_tmp = path_util.pure_path_join(output, "tmp")


def re_mkdir(rm_output=False) -> None:
    dirs = [output_tmp, output_api, output_web, output_app, output_db_bak, output_db_all_in_one]
    if rm_output:
        shutil.rmtree(path=output, ignore_errors=True)
        logger.info(basic_util.action_formatter(re_mkdir.__name__, dirs.__str__()))
    [Path(p).mkdir(parents=True, exist_ok=True) for p in dirs]
