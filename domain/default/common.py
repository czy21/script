#!/usr/bin/env python3
from script.domain.default import path as default_path
from script.utility import collection as list_util
from script.utility import path as path_util

param_project_name = ""
param_env_suffix = ""

param_template_output_dict = {}

param_main_db_name = ""
param_main_db_bak_name = ""

# mysql
param_main_db_mysql_name = ""
param_main_db_mysql_host = ""
param_main_db_mysql_port = ""
param_main_db_mysql_user = ""
param_main_db_mysql_pass = ""
param_main_db_mysql_file_path = ""

# pgsql
param_main_db_pgsql_name = ""
param_main_db_pgsql_host = ""
param_main_db_pgsql_port = ""
param_main_db_pgsql_user = ""
param_main_db_pgsql_pass = ""
param_main_db_pgsql_file_path = ""

# cksql
param_main_db_cksql_name = ""
param_main_db_cksql_host = ""
param_main_db_cksql_port = ""
param_main_db_cksql_user = ""
param_main_db_cksql_pass = ""
param_main_db_cksql_file_path = ""

# mssql
param_main_db_mssql_file_path = ""

# neo4j
param_main_db_neo4j_name = ""
param_main_db_neo4j_host = ""
param_main_db_neo4j_port = ""
param_main_db_neo4j_user = ""
param_main_db_neo4j_pass = ""
param_main_db_neo4j_file_path = ""

# mongo
param_main_db_mongo_name = ""
param_main_db_mongo_host = ""
param_main_db_mongo_port = ""
param_main_db_mongo_user = ""
param_main_db_mongo_pass = ""
param_main_db_mongo_file_path = ""

param_main_redis_host = ""
param_main_rabbit_host = ""

# api
param_api_archive_file_name = "api.jar"
param_api_root_project_path = ""
param_api_gradle_init_script_file_path = path_util.pure_path_join(default_path.script_template, "java/init.gradle")
param_api_gradle_plugin_root_project_path = default_path.project_plugin
param_api_module_name = ""

# api output
param_api_output_path = default_path.output_api

# web
param_web_output_path = default_path.output_web
param_web_root_project_path = ""
