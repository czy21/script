import itertools

import numpy as np
import pandas as pd
import config, uuid
from cerberus import errors, Validator

from datetime import datetime
from pymongo import MongoClient
from sqlalchemy import create_engine

engine = create_engine(config.MYSQL_HOST)
mongoClient = MongoClient(host=config.MONGO_HOST)

startTime = datetime.now()
print("start time:", startTime)

flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) else [L]


def validate(series, mapping_list: list):
    error_msgs = []

    for t in mapping_list:
        for s in t.get("validators", []):
            header = t["header"]
            schema = {header: s.get("schema", {})}
            message = s.get("message", "")
            cell = None if pd.isna(series.get(header)) else series.get(header)

            class MessageErrorHandler(errors.BasicErrorHandler):
                messages = errors.BasicErrorHandler.messages.copy()
                messages[errors.REQUIRED_FIELD.code] = message
                messages[errors.NOT_NULLABLE.code] = message
                messages[errors.BAD_TYPE.code] = message

            v = Validator(schema, error_handler=MessageErrorHandler)
            v.validate({header: cell})
            error_msgs.append(list(v.errors.values()))

    return ",".join(flat(list(error_msgs)))


def map_schema(item):
    item["validators"] = list(map(lambda v: {"schema": v, "message": v.pop("message")}, item.get("validators", [])))
    return item


with pd.ExcelFile(path_or_buffer="1K.xlsx") as f:
    table = mongoClient["spi_local"]["ent_file_column_mapping"]
    sd_mapping_list = list(map(map_schema, table.find_one({"businessType": "SD"})["fields"]))
    sd_mapping_dict = dict((t["header"], t["column"]) for t in sd_mapping_list)
    df = pd.read_excel(f, "SD")
    df["错误"] = df.apply(lambda x: validate(x, sd_mapping_list), axis=1)

    resolve_time = datetime.now()
    print("解析耗时:", (resolve_time - startTime).seconds)

    if df["错误"].isnull().all():
        except_columns = list(filter(lambda c: c not in sd_mapping_dict.keys(), df.columns))
        df.drop(columns=except_columns, inplace=True)
        df.rename(columns=sd_mapping_dict, inplace=True)
        df["file_id"] = uuid.uuid4()
        df["id"] = df.apply(lambda _: uuid.uuid4(), axis=1)
        df["row_number"] = df.apply(lambda x: (x.name + 1), axis=1)
        df.to_sql(name="ent_sfl_inspect_sale", con=engine, if_exists="replace", index=False)
    else:
        print("有错误")
        df.to_excel("error.xlsx", index=False)

endtime = datetime.now()
print("end time:", endtime)

seconds = (endtime - startTime).seconds
print("总耗时: ", seconds)
