#!/usr/bin/env python3
from pathlib import Path

from script.utility import path as path_util

root_path = path_util.pure_path_join("../../")
output = path_util.pure_path_join(root_path, "___output")
project_code = path_util.pure_path_join(root_path, "code")
project_db = path_util.pure_path_join(root_path, "db")

# child dir of code
project_code_api = path_util.pure_path_join(project_code, "api")
project_code_web = path_util.pure_path_join(project_code, "web")
project_code_app = path_util.pure_path_join(project_code, "app")

# child dir of output
output_api = path_util.pure_path_join(output, "api")
output_api_resource = path_util.pure_path_join(output_api, "resources")
output_web = path_util.pure_path_join(output, "web")
output_app = path_util.pure_path_join(output, "app")
output_db = path_util.pure_path_join(output, "db")
output_db_bak = path_util.pure_path_join(output_db, "bak")
output_db_all_in_one = path_util.pure_path_join(output_db, "all_in_one")

output_db_all_in_one_mongo = path_util.pure_path_join(output_db_all_in_one, "mongo.mongo")
output_db_all_in_one_mysql = path_util.pure_path_join(output_db_all_in_one, "mysql.mysql")
output_db_all_in_one_mssql = path_util.pure_path_join(output_db_all_in_one, "mssql.mssql")
output_db_all_in_one_neo4j = path_util.pure_path_join(output_db_all_in_one, "neo4j.neo4j")
output_tmp = path_util.pure_path_join(output, "tmp")


def mkdir(path) -> None:
    for p in path:
        if not Path(p).exists():
            Path(p).mkdir(parents=True)


mkdir([output_tmp, output_api_resource, output_web, output_app, output_db_bak, output_db_all_in_one])
