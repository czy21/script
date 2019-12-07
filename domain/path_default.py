# !/usr/bin/env python
from pathlib import Path

root_path = Path('../../').as_posix()
output = Path(root_path).resolve().joinpath("___output").as_posix()
project_code = Path(root_path).resolve().joinpath("code").as_posix()
project_db = Path(root_path).resolve().joinpath("db").as_posix()

# child dir of code
project_code_api = Path(project_code).resolve().joinpath("api").as_posix()
project_code_web = Path(project_code).resolve().joinpath("web").as_posix()
project_code_app = Path(project_code).resolve().joinpath("app").as_posix()

# child dir of db
project_db_create = Path(project_db).resolve().joinpath("create").as_posix()
project_db_create_prepare = Path(project_db_create).resolve().joinpath("1_prepare").as_posix()
project_db_create_version = Path(project_db_create).resolve().joinpath("2_version").as_posix()

# child dir of output
output_api = Path(output).resolve().joinpath("api").as_posix()
output_web = Path(output).resolve().joinpath("web").as_posix()
output_app = Path(output).resolve().joinpath("app").as_posix()
output_db = Path(output).resolve().joinpath("db").as_posix()
output_db_bak = Path(output_db).resolve().joinpath("bak").as_posix()
output_db_all_in_one = Path(output_db).resolve().joinpath("all_in_one").as_posix()
output_db_all_in_one_mysql = Path(output_db_all_in_one).resolve().joinpath("mysql.mysql").as_posix()
output_tmp = Path(output).resolve().joinpath("tmp").as_posix()


def mkdir(path):
    for p in path:
        if not Path(p).exists():
            Path(p).mkdir(parents=True)


paths = [output_tmp, output_api, output_web, output_app, output_db_bak, output_db_all_in_one]
mkdir(paths)
