#!/usr/bin/env python3
from script.domain.default import path as default_path

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
param_api_archive_file_name = ""
param_api_network_name = ""
param_api_network_containers = []
param_api_image = ""
param_api_root_project_path = ""
param_api_docker_gradle_command = True
param_api_gradle_init_script_file_path = ""
param_api_plugin_file_path = ""

param_api_gradle_extra_config_template_path = ""
param_api_gradle_extra_config_output_path = ""
param_api_config_file_output_path = ""
param_api_dockerfile_output_path = ""
param_api_compose_file_output_path = ""

# api output
param_api_output_path = default_path.output_api

# web
param_web_output_path = default_path.output_web
param_web_root_project_path = ""

param_web_cp_template_path = ""
param_web_cp_output_file_path = ""

param_web_nginx_template_path = ""
param_web_nginx_output_file_path = ""

param_web_env_template_path = ""
param_web_env_path = ""
