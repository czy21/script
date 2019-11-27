# !/usr/bin/env python

from pathlib import Path

root_path = str(Path('../../'))
output = str(Path(root_path).resolve().joinpath("___output"))
project_code = str(Path(root_path).resolve().joinpath("code"))
project_db = str(Path(root_path).resolve().joinpath("db"))

# child dir of code
project_code_api = str(Path(project_code).resolve().joinpath("api"))
project_code_web = str(Path(project_code).resolve().joinpath("web"))
project_code_app = str(Path(project_code).resolve().joinpath("app"))

# child dir of db
project_db_create = str(Path(project_db).resolve().joinpath("create"))
project_db_create_prepare = str(Path(project_db_create).resolve().joinpath("1_prepare"))
project_db_create_version = str(Path(project_db_create).resolve().joinpath("2_version"))

# child dir of output
output_api = str(Path(output).resolve().joinpath("api"))
output_web = str(Path(output).resolve().joinpath("web"))
output_app = str(Path(output).resolve().joinpath("app"))
output_db = str(Path(output).resolve().joinpath("db"))
output_db_bak = str(Path(output_db).resolve().joinpath("bak"))
output_db_all_in_one = str(Path(output_db).resolve().joinpath("all_in_one"))
output_db_all_in_one_mysql = str(Path(output_db_all_in_one).resolve().joinpath("mysql.mysql"))


def mkdir(path):
    for p in path:
        if not Path(p).exists():
            Path(p).mkdir(parents=True)


paths = [output_api, output_web, output_app, output_db_bak, output_db_all_in_one]
mkdir(paths)
