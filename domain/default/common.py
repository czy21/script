#!/usr/bin/env python3

param_main_db_host = ""
param_main_db_name = ""
param_main_db_bak_name = ""

# mysql
param_main_db_mysql_port = ""
param_main_db_mysql_user = ""
param_main_db_mysql_pass = ""
param_main_db_mysql_file_path = ""

# mssql
param_main_db_mssql_file_path = ""

# neo4j
param_main_db_neo4j_db_name = ""
param_main_db_neo4j_port = ""
param_main_db_neo4j_user = ""
param_main_db_neo4j_pass = ""
param_main_db_neo4j_file_path = ""

# mongo
param_main_db_mongo_port = ""
param_main_db_mongo_user = ""
param_main_db_mongo_pass = ""
param_main_db_mongo_file_path = ""

# api
param_api_archive_file_name = ""
param_api_extra_config_template_name = ""
param_api_yml_override_template_name = ""
param_api_root_project_path = ""
param_api_output_path = ""
param_api_output_resource_path = ""
param_api_docker_gradle_command = ""
param_api_gradle_init_script_file_path = ""
param_api_plugin_path = ""

# tmp
param_tmp_api_extra_config_template_name = ""

# injected
param_injected = {}


def get_params():
    return dict({k: v for k, v in globals().items() if isinstance(v, str) and k.startswith("param")}, **param_injected)
