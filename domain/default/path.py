#!/usr/bin/env python3
import pathlib

root_path = pathlib.Path(__file__, "../../../../").resolve()
output_path = pathlib.Path(root_path, "___output")

source_db = pathlib.Path(root_path, "db")

output_db = pathlib.Path(output_path, "db")
output_db_bak = pathlib.Path(output_db, "bak")
output_db_all_in_one = pathlib.Path(output_db, "all_in_one")

output_db_all_in_one_mysql = pathlib.Path(output_db_all_in_one, "mysql.sql")
output_db_all_in_one_pgsql = pathlib.Path(output_db_all_in_one, "pgsql.sql")
output_db_all_in_one_mssql = pathlib.Path(output_db_all_in_one, "mssql.sql")
output_db_all_in_one_chsql = pathlib.Path(output_db_all_in_one, "chsql.sql")
output_db_all_in_one_mongo = pathlib.Path(output_db_all_in_one, "mongo.mongo")
output_db_all_in_one_neo4j = pathlib.Path(output_db_all_in_one, "neo4j.neo4j")

output_db_bak_gz_mysql = pathlib.Path(output_db_bak, "mysql.gz")
output_db_bak_gz_pgsql = pathlib.Path(output_db_bak, "pgsql.gz")
output_db_bak_gz_mssql = pathlib.Path(output_db_bak, "mssql.gz")
output_db_bak_gz_mongo = pathlib.Path(output_db_bak, "mongo.gz")

output_db_bak_sql_mysql = pathlib.Path(output_db_bak, "mysql.sql")
output_db_bak_sql_pgsql = pathlib.Path(output_db_bak, "pgsql.sql")
output_db_bak_sql_mssql = pathlib.Path(output_db_bak, "mssql.sql")
output_db_bak_sql_mongo = pathlib.Path(output_db_bak, "mongo.sql")

output_tmp = pathlib.Path(output_path, "tmp")


def create_dir() -> None:
    dirs = [output_tmp, output_db_bak, output_db_all_in_one]
    for p in dirs:
        pathlib.Path(p).mkdir(parents=True, exist_ok=True)
