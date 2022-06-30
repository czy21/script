import os
import uuid
from datetime import datetime
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine

import config
from script.utility import path as path_util

engine = create_engine(config.MYSQL_HOST)
mongoClient = MongoClient(host=config.MONGO_HOST)


def validate(series, mapping_list: list):
    error_msgs = []

    for t in mapping_list:
        for s in t.get("validators", []):
            header = t["header"]
            cell = series.get(header)
            v_message = s.get("message", "")
            v_required = s.get("required", False)
            v_type = s.get("type")
            if v_required and pd.isna(cell):
                error_msgs.append(v_message)
                break
            if not pd.isna(v_type):
                if (v_type == "integer" or v_type == "float") and not pd.api.types.is_number(cell):
                    error_msgs.append(v_message)
                if v_type == "date" and not isinstance(cell, datetime):
                    error_msgs.append(v_message)
    return ",".join(error_msgs) if error_msgs else np.nan


table = mongoClient["spi_local"]["ent_file_column_mapping"]


def resolve_file(file_path: str, file_definitions: list, error_output_path: str):
    print('子进程: {} - 任务{}'.format(os.getpid(), file_path))

    with pd.ExcelFile(path_or_buffer=file_path) as f:
        exist_definition_dicts = dict((d["businessType"], d) for d in filter(lambda t: t["businessType"] in f.sheet_names, file_definitions))
        df_dict = pd.read_excel(f, sheet_name=list(exist_definition_dicts.keys()))
        error_path = path_util.join_path(error_output_path, Path(file_path).name)
        for d in df_dict.items():
            resolve_sheet(d, exist_definition_dicts.get(d[0]), error_path)


def resolve_sheet(dfd: dict, file_definition: dict, error_file_path):
    sheet_name = dfd[0]
    df = dfd[1]
    table_name = file_definition["tableName"]
    mapping_fields = file_definition["fields"]
    mapping_dict = dict((t["header"], t["column"]) for t in mapping_fields)
    df["错误"] = df.apply(lambda x: validate(x, mapping_fields), axis=1)
    if df["错误"].isnull().all():
        except_columns = list(filter(lambda c: c not in mapping_dict.keys(), df.columns))
        df.drop(columns=except_columns, inplace=True)
        df.rename(columns=mapping_dict, inplace=True)
        df["file_id"] = uuid.uuid4()
        df["id"] = df.apply(lambda _: uuid.uuid4(), axis=1)
        df["row_number"] = df.apply(lambda x: (x.name + 1), axis=1)
        df.to_sql(name=table_name, con=engine, if_exists="append", index=False, chunksize=10000)
    else:
        print("有错误")
        df.to_excel(error_file_path, sheet_name=sheet_name, index=False)
    del df


if __name__ == '__main__':

    start_time = datetime.now()
    print("start time:", start_time)

    all_excel_list = list(map(lambda p: p.resolve().as_posix(), Path("./files").glob("*")))
    error_output_path = path_util.join_path("./errors")
    file_mapping_definition = list(table.find())
    p = Pool(4)
    for f in all_excel_list:
        p.apply_async(resolve_file, args=(f, file_mapping_definition, error_output_path,))
    p.close()
    p.join()
    end_time = datetime.now()
    print("end time:", end_time)

    seconds = (end_time - start_time).seconds
    print("总耗时: ", seconds)
