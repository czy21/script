import itertools
import os

import numpy as np
import pandas as pd
import config, uuid
from cerberus import errors, Validator

from datetime import datetime
from pymongo import MongoClient
from sqlalchemy import create_engine

engine = create_engine(config.MYSQL_HOST)
mongoClient = MongoClient(host=config.MONGO_HOST)

start_time = datetime.now()
print("start time:", start_time)


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


file_dir = "./files"
all_excel_list = os.listdir(file_dir)

table = mongoClient["spi_local"]["ent_file_column_mapping"]
sd_fields = table.find_one({"businessType": "SD"})["fields"]
for aes in all_excel_list:

    with pd.ExcelFile(path_or_buffer=aes) as f:
        mapping_list = sd_fields
        mapping_dict = dict((t["header"], t["column"]) for t in mapping_list)
        df = pd.read_excel(f, "SD")
        df["错误"] = df.apply(lambda x: validate(x, mapping_list), axis=1)

        resolve_time = datetime.now()
        print("解析耗时:", (resolve_time - start_time).seconds)

        if df["错误"].isnull().all():
            except_columns = list(filter(lambda c: c not in mapping_dict.keys(), df.columns))
            df.drop(columns=except_columns, inplace=True)
            df.rename(columns=mapping_dict, inplace=True)
            df["file_id"] = uuid.uuid4()
            df["id"] = df.apply(lambda _: uuid.uuid4(), axis=1)
            df["row_number"] = df.apply(lambda x: (x.name + 1), axis=1)
            df.to_sql(name="ent_sfl_inspect_sale", con=engine, if_exists="replace", index=False)
        else:
            print("有错误")
            df.to_excel("error.xlsx", index=False)

end_time = datetime.now()
print("end time:", end_time)

seconds = (end_time - start_time).seconds
print("总耗时: ", seconds)
