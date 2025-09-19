#!/usr/bin/env python3
import pathlib

root_path = pathlib.Path(__file__, "../../../../").resolve()
output_path = pathlib.Path(root_path, "___output")

source_db = pathlib.Path(root_path, "db")

output_db = pathlib.Path(output_path, "db")
output_db_bak = pathlib.Path(output_db, "bak")
output_db_all_in_one = pathlib.Path(output_db, "all_in_one")

output_tmp = pathlib.Path(output_path, "tmp")

def create_dir() -> None:
    dirs = [output_tmp, output_db_bak, output_db_all_in_one]
    for p in dirs:
        pathlib.Path(p).mkdir(parents=True, exist_ok=True)
