# !/usr/bin/env python
from script.domain.default import path as default_path
from script.utility import path as path_util

param_main_db_host = ""
param_main_db_name = ""
param_main_db_bak_name = ""

# mysql
param_main_db_mysql_port = ""
param_main_db_mysql_user = ""
param_main_db_mysql_pass = ""
param_main_db_mysql_file_path = path_util.pure_path_join(default_path.project_db, "mysql")
param_main_db_mysql_output_file_name = default_path.output_db_all_in_one_mysql

# mssql
param_main_db_mssql_file_path = path_util.pure_path_join(default_path.project_db, "mssql")
param_main_db_mssql_output_file_name = default_path.output_db_all_in_one_mssql

# neo4j
param_main_db_neo4j_db_name = ""
param_main_db_neo4j_port = ""
param_main_db_neo4j_user = ""
param_main_db_neo4j_pass = ""
param_main_db_neo4j_file_path = path_util.pure_path_join(default_path.project_db, "neo4j")
param_main_db_neo4j_output_file_name = default_path.output_db_all_in_one_neo4j

# mongo
param_main_db_mongo_port = ""
param_main_db_mongo_user = ""
param_main_db_mongo_pass = ""
param_main_db_mongo_file_path = path_util.pure_path_join(default_path.project_db, "mongo")
param_main_db_mongo_output_file_name = default_path.output_db_all_in_one_mongo

# api
param_api_archive_file_name = "api.jar"
param_api_extra_config_template_name = ""
param_api_yml_override_template_name = ""
param_api_root_project_path = ""
param_api_output_path = default_path.output_api
param_api_output_resource_path = default_path.output_api_resource

# tmp
param_tmp_api_extra_config_template_name = ""

# injected
param_injected = {}


def get_params():
    return dict({k: v for k, v in globals().items() if isinstance(v, str) and k.startswith("param")}, **param_injected)
